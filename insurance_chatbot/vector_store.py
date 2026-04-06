def upload_or_delete_documents():
    """Function to handle the Upload Documents page."""
    st.title("📤 Upload Documents")
    st.write("*Upload your insurance-related documents to fine-tune the AI chatbot.*")
    placeholder1 = st.empty()
    placeholder2 = st.empty()
    st.write("#### Exixting Uploaded Files:")
    # File uploader for multiple files
    uploaded_files = st.sidebar.file_uploader(
        "Upload a file",
        type=["txt", "pdf", "docx"],
        label_visibility="collapsed",
        accept_multiple_files=True
    )
    if uploaded_files:
        for uploaded_file in uploaded_files:
            placeholder1.write(f"- {uploaded_file.name}")
            time.sleep(0.2)  # Simulate processing time
    else:
        st.info("No files uploaded yet. Please upload your documents.")
    placeholder1.empty()  # Clear the placeholder after displaying the file names
    
    if st.sidebar.button("upload files"):
        
        counter = 0
        for uploaded_file in uploaded_files:
            
            # Process each uploaded file (placeholder for actual processing logic)
            doc=process_doc(uploaded_file,uploaded_file.type)
            # print(len(doc[1]))
            total_chunks = 0
            if doc[0]:
                counter += 1
                placeholder1.success(f"Processed: {uploaded_file.name}")
                for page in doc[1]:
                    flag,chunk_number=westore(page["text"],page["page_number"],uploaded_file.name)
                    if flag:
                        total_chunks += chunk_number
                    else:
                        placeholder2.error(message)
                if flag:
                    placeholder2.success(f"uploaded {total_chunks} chunks from {uploaded_file.name} to vector database")
                time.sleep(0.5)
            else:
                placeholder1.error(f"Error processing {uploaded_file.name}: {doc[1]}")

              # Simulate processing time
            
        if counter == len(uploaded_files):
            placeholder2.success(f"Processed all uploaded files successfully!")

    if st.sidebar.button("delete all files from vector database"):
        flag,message=wedel()
        if flag:
            placeholder2.success(message)
        else:
            placeholder2.error(message)