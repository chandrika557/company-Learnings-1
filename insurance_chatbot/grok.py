import weaviate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
from weaviate.collections.classes.filters import Filter
import os

# Function to create/connect to Weaviate client and collection
def get_weaviate_collection(collection_name="insurance_data"):
    weaviate_url = os.environ.get("WEAVIATE_URL")
    weaviate_key = os.environ.get("WEAVIATE_API_KEY")

    if not weaviate_url or not weaviate_key:
        raise ValueError("WEAVIATE_URL and WEAVIATE_API_KEY must be set in environment variables.")

    # Initialize Weaviate client
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_key),
    )

    if not client.is_ready():
        raise ConnectionError("Weaviate client is not ready.")

    # Create collection if it doesn’t exist
    if not client.collections.exists(collection_name):
        try:
            client.collections.create(
                name=collection_name,
                properties=[
                    Property(name="chunk_id", data_type=DataType.TEXT),
                    Property(name="description", data_type=DataType.TEXT),
                    Property(name="filename", data_type=DataType.TEXT),
                    Property(name="page_number", data_type=DataType.INT),
                ],
                vectorizer_config=[
                    Configure.NamedVectors.text2vec_weaviate(
                        name="vectors",
                        source_properties=["description"],
                        model="Snowflake/snowflake-arctic-embed-m-v1.5",
                        dimensions=768,
                    )
                ],
            )
            print(f"Created collection '{collection_name}'.")
        except Exception as e:
            client.close()
            raise ValueError(f"Failed to create collection '{collection_name}': {str(e)}")

    collection = client.collections.get(collection_name)
    return client, collection

# Function to store text chunks in Weaviate
def weaviate_store(text, page_number, filename, collection_name="insurance_data"):
    client, collection = get_weaviate_collection(collection_name)

    try:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=80)
        chunks = text_splitter.split_text(text)

        # Batch import chunks
        with collection.batch.dynamic() as batch:
            for i, chunk in enumerate(chunks):
                batch.add_object(
                    properties={
                        "chunk_id": f"{filename}-chunk-{i}",
                        "description": chunk,
                        "filename": filename,
                        "page_number": page_number,
                    },
                )

        # Check for failed imports
        failed_objects = collection.batch.failed_objects
        if failed_objects:
            return False, f"Batch import failed with {len(failed_objects)} errors: {failed_objects[0]}"
        else:
            return True, f"Successfully imported {len(chunks)} chunks from {filename}."

    except Exception as e:
        return False, f"An error occurred while storing data: {str(e)}"
    finally:
        client.close()

# Function to query stored chunks
def weaviate_query(query_text, limit=2, collection_name="insurance_data"):
    client, collection = get_weaviate_collection(collection_name)

    try:
        # Perform a near-text query
        response = collection.query.near_text(
            query=query_text,
            limit=limit,
        )

        # Process and display results
        if not response.objects:
            return False, "No matching chunks found."
        else:
            result = []
            file_names = []
            print(f"Found {len(response.objects)} matching chunks:")
            for obj in response.objects:
                result.append(obj.properties['description'])
                filename = obj.properties['filename']
                page_number = obj.properties['page_number']
                if not any(fn['filename'] == filename for fn in file_names):
                    file_names.append({"filename": filename, "page_number": page_number})
            return True, {"descriptions": result, "file_names": file_names}

    except Exception as e:
        return False, f"An error occurred while querying: {str(e)}"
    finally:
        client.close()

# Function to delete vectors from the collection
def weaviate_delete(uuid_to_delete=None, filename=None, chunk_id=None, collection_name="insurance_data"):
    client, collection = get_weaviate_collection(collection_name)
    try:
        if not any([uuid_to_delete, filename, chunk_id]):
            client.collections.delete(collection_name)
            return True, f"Deleted the entire collection: {collection_name}"

        if uuid_to_delete:
            collection.data.delete_by_id(uuid_to_delete)
            return True, f"Deleted object with UUID: {uuid_to_delete}"

        elif chunk_id:
            response = collection.query.fetch_objects(
                filters=Filter.by_property("chunk_id").equal(chunk_id),
                limit=1
            )
            if not response.objects:
                return False, f"No chunk found with ID: {chunk_id}"
            else:
                uuid = response.objects[0].uuid
                collection.data.delete_by_id(uuid)
                return True, f"Deleted chunk with ID: {chunk_id} (UUID: {uuid})"

        elif filename:
            response = collection.query.fetch_objects(
                filters=Filter.by_property("filename").equal(filename),
                limit=1000
            )
            deleted_count = 0
            for obj in response.objects:
                collection.data.delete_by_id(obj.uuid)
                deleted_count += 1
            if deleted_count == 0:
                return False, f"No chunks found for filename: {filename}"
            else:
                return True, f"Deleted {deleted_count} chunks associated with filename: {filename}"

    except Exception as e:
        return False, f"An error occurred while deleting: {str(e)}"
    finally:
        client.close()

# Example usage
if __name__ == "__main__":
    pass