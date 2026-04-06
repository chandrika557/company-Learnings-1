import json
import os
from datetime import datetime

JSON_FILE = "uploaded_files.json"

def load_json():
    """Load the JSON file or return an empty dictionary if it doesn't exist or is corrupted."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON file: {e}. Returning empty dictionary.")
            return {}
    return {}

def save_json(data):
    """Save the given data to the JSON file."""
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving JSON file: {e}")

def add_file_to_json(filename, chunk_count, collection_name="insurance_data"):
    """Add or update a file entry in the JSON file."""
    data = load_json()
    data[filename] = {
        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "stored",
        "chunk_count": chunk_count,
        "collection_name": collection_name,
    }
    save_json(data)

def remove_file_from_json(filename):
    """Remove a file entry from the JSON file."""
    data = load_json()
    if filename in data:
        del data[filename]
        save_json(data)
        return True
    return False

def clear_collection_from_json(collection_name):
    """Remove all file entries associated with the given collection from the JSON file."""
    data = load_json()
    updated = False
    for filename in list(data.keys()):
        if data[filename].get("collection_name") == collection_name:
            del data[filename]
            updated = True
    if updated:
        save_json(data)
    return updated