import streamlit as st
import time
import pandas as pd
from datetime import datetime
from agent import chat_with_llama , chat_with_llama_direct, gemini_ai
from doc_handler import process_doc, generate_analysis_pdf, markdown_to_pdf
from vector_store2 import weaviate_store as westore ,weaviate_delete as wedel , weaviate_query as wequery
from ledger import add_file_to_json, remove_file_from_json, clear_collection_from_json, load_json
from prompt import insurance_query as incq, summarize_context as sumcon, claim_query as cq
import base64
import os

# Assume files are stored in a temporary directory after upload


def get_base64_of_file(file_path):
    """Convert file to base64 for embedding in HTML."""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return None


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def chat_bot():

    st.title("🤖 Insurance Chatbot - Your AI Assistant")
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display existing chat history
    for message in st.session_state["chat_history"]:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").markdown(message["content"], unsafe_allow_html=True)

    # Ensure chat history does not exceed 10 messages
    

    # Chat input for user messages
    prompt = st.chat_input(placeholder="Ask about insurance, claims, or premiums...")
    if prompt:
        # Add user message to chat history
        result=[]
        # file_names=[]
        file_pages = {}
        st.chat_message("user").write(prompt)
        retrival_flag,data= wequery(prompt,limit=10)
        if retrival_flag:
            # print(data)
            result,file_data=data
            for i in file_data:
                filename = i["filename"]
                page_number = i["page_number"]
                if filename not in file_pages:
                    file_pages[filename] = set()
                file_pages[filename].add(page_number)     

        # Create a placeholder for the assistant's response
        assistant_message = st.chat_message("assistant")
        response_placeholder = assistant_message.empty()

        # Stream the response from the Llama model
        response_text = ""  # To store the full response
        
        # if "chat_history" in st.session_state: 
        #     summary = chat_with_llama_direct(sumcon(st.session_state["chat_history"]))
        #     print(summary)
        retrived_data="\n".join(
                f"Document-{i}: {data.strip()}"
                for i,data in enumerate(result)
            )
        print(retrived_data)
        query=incq(prompt,retrived_data)
        # print(query)
        st.session_state["chat_history"].append({"role": "user", "content": prompt})

        # for chunk in chat_with_llama(query):
        for chunk in gemini_ai(query):
            response_text += chunk  # Append each chunk to the full response
            response_placeholder.write(response_text)  # Update the placeholder progressively

        # Format and append the file names to the response
        if file_pages:
            file_list = []
            for filename, pages in file_pages.items():
                pages_str = ", ".join(map(str, sorted(pages)))
                # Use an emoji as an icon, with a tooltip
                                # Check if file exists in JSON ledger and get its path
                
                file_path = fr"C:\practice\insurance_chatbot\insurance_docs\{filename.strip()}"
                if os.path.exists(file_path):
                    # Convert file to base64 for embedding
                    file_base64 = get_base64_of_file(file_path)
                    if file_base64:
                        # Create a data URL for the file
                        mime_type = "application/pdf" if filename.lower().endswith(".pdf") else "text/plain"
                        data_url = f"data:{mime_type};base64,{file_base64}"
                        # Create clickable icon with tooltip
                        file_list.append(
                            f'<a href="{data_url}" target="_blank" title="{filename} (Pages: {pages_str})" style="cursor: pointer; text-decoration: none;">📄</a>'
                        )
                    else:
                        file_list.append(
                            f'<span title="{filename} (Pages: {pages_str}) - File not accessible" style="cursor: not-allowed;">📄</span>'
                        )
                else:
                    file_list.append(
                        f'<span title="{filename} (Pages: {pages_str}) - File not found" style="cursor: not-allowed;">📄</span>'
                    )

                # file_list.append(f"<span title='{filename} (Pages: {pages_str})' style='cursor: pointer;'>📄</span>")
            file_message = f"**Data retrieved from:** {' '.join(file_list)}"
            assistant_message.markdown(response_text + "\n\n---\n" + file_message, unsafe_allow_html=True)
        else:
            assistant_message.markdown(response_text)
        # if file_pages:
        #     file_list = []
        #     for filename, pages in file_pages.items():
        #         pages_str = ", ".join(map(str, sorted(pages)))
        #         file_list.append(f"<span title='Pages: {pages_str}' style='cursor: pointer;'>📄 {filename}</span>")
        #     file_message = f"**Data retrieved from:** {', '.join(file_list)}"
        #     assistant_message.markdown(response_text + "\n\n---\n" + file_message, unsafe_allow_html=True)
        # else:
        #     assistant_message.write(response_text)
        # Add the full assistant response to chat history
        st.session_state["chat_history"].append({"role": "assistant", "content": response_text + "\n\n---\n" + file_message})

def login_page():
    """Login page for the Insurance Chatbot."""
    st.markdown("<h2 style='text-align: center;'>🔐 Login to Insurance Chatbot</h2>", unsafe_allow_html=True)
    
    # Center the login form using columns
    col1, col2, col3 = st.columns([2, 5, 2])
    with col2:
        with st.form("login_form"):
            # Input fields for username and password
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password") 
            # Login button
            submitted = st.form_submit_button("Login")
           
            if submitted:
                if username == "admin" and password == "password123":  # Replace with your authentication logic
                    st.session_state['logged_in'] = True  # Update login state
                    st.success("Login successful! Redirecting...")
                    time.sleep(0.6)  # Simulate a delay for redirection
                    st.rerun()  # Redirect to the main page
                else:
                    st.error("Invalid credentials. Please try again.")

def claims_analysis_and_premium_calculator():
    """Function to handle Claims Analysis and Premium Calculator page."""
    st.title("📊 Claims Analysis & Premium Calculator")
    
    # Insurance type selection
    insurance_types = ["Auto", "Health", "Home", "Life", "Travel"]
    insurance_type = st.selectbox("Select Insurance Type", insurance_types)
    
    # Initialize required fields based on insurance type
    required_fields = {
        "Auto": [
            "Age", "Vehicle Make", "Vehicle Model", "Vehicle Year", "Driving History (years)", 
            "Annual Mileage", "Driving Record (e.g., number of accidents)", 
            "Claim History (number of previous claims)", "Vehicle History (e.g., accidents, repairs)",
            "Present Vehicle Value"
        ],
        "Health": [
            "Age", "Pre-existing Conditions", "Smoking Status", "Height (cm)", "Weight (kg)", 
            "Medical History (e.g., chronic diseases)", "Claim History (number of previous claims)"
        ],
        "Home": [
            "Property Value", "Present Property Value", "Property Address", "Home Age", 
            "Security Features", "Square Footage", "Claim History (number of previous claims)", 
            "Personal Property Value", "House Type (e.g., HO-1, HO-2, HO-3, HO-5)"
        ],
        "Life": [
            "Age", "Occupation", "Annual Income", "Health Status", "Coverage Amount", 
            "Claim History (number of previous claims)"
        ],
        "Travel": [
            "Trip Duration (days)", "Destination", "Trip Cost", "Traveler Age", 
            "Medical Conditions", "Coverage Type (e.g., cancellation, medical)", 
            "Claim History (number of previous claims)"
        ]
    }
    
    # Create form for required fields
    st.subheader("Enter Your Details")
    user_data = {}
    with st.form("user_details_form"):
        st.subheader(f"{insurance_type} Insurance Details")
        user_data = {}
        for field in required_fields[insurance_type]:
            if field in ["Age", "Annual Mileage", "Height (cm)", "Weight (kg)", "Property Value", 
                         "Present Property Value", "Present Vehicle Value", "Home Age", 
                         "Square Footage", "Annual Income", "Coverage Amount", 
                         "Driving History (years)", "Claim History (number of previous claims)", 
                         "Trip Duration (days)", "Trip Cost"]:
                user_data[field] = st.number_input(field, min_value=0.0, step=1.0)
            elif field == "House Type (e.g., HO-1, HO-2, HO-3, HO-5)":
                user_data[field] = st.selectbox(field, ["HO-1", "HO-2", "HO-3", "HO-5"])
            else:
                user_data[field] = st.text_input(field)
        # File uploader for policy document
        policy_doc = st.file_uploader("Upload Policy Document", type=['pdf', 'doc', 'docx'])
        
        submitted = st.form_submit_button("Analyze Claims & Calculate Premium")
        
    if submitted :
        with st.spinner("Processing your data..."):
            # Process the uploaded document
            # doc_content = process_doc(policy_doc,policy_doc.type)
            text_palceholder=st.empty()
            response_text = ""
            # Get analysis from Ollama
            for chunk in chat_with_llama(cq(insurance_type, user_data, doc_content=policy_doc)):
                response_text += chunk  # Append each chunk to the full response
                text_palceholder.write(response_text,unsafe_allow_html=True)  # Update the placeholder progressively
                   
                # Download button for PDF
            st.download_button(
                label="📥 Download Analysis Report",
                data=markdown_to_pdf(response_text),  # Assuming this function converts the response to PDF
                file_name=f"Insurance_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

def claims_and_premium_calculator():
    """Function to handle Claims Analysis and Premium Calculator page."""
    st.title("📊 Claims Analysis & Premium Calculator")
    
    # Insurance type selection
    insurance_types = ["Auto", "Health", "Home", "Life"]
    insurance_type = st.selectbox("Select Insurance Type", insurance_types)
    
    # Essential common policy information
    st.subheader("Policy Information")
    policy_number = st.text_input("Policy Number")
    effective_date = st.date_input("Effective Date")
    expiration_date = st.date_input("Expiration Date")
    coverage_type = st.text_input("Coverage Type (e.g., liability, collision)")
    coverage_limits = st.number_input("Coverage Limits", min_value=0.0, step=1000.0)
    deductible = st.number_input("Deductible Amount", min_value=0.0, step=100.0)
    policy_discounts = st.text_input("Policy Discounts (e.g., multi-policy, low-mileage, comma-separated)")

    # Store common data
    common_data = {
        "Policy Number": policy_number,
        "Effective Date": effective_date,
        "Expiration Date": expiration_date,
        "Coverage Type": coverage_type,
        "Coverage Limits": coverage_limits,
        "Deductible Amount": deductible,
        "Policy Discounts": policy_discounts
    }
    
    # Define required fields for each insurance type
    required_fields = {
        "Auto": [
            "Age", "Vehicle Make", "Vehicle Model", "Vehicle Year", "Driving History (years)", 
            "Annual Mileage", "Driving Record (e.g., number of accidents)", "Claim History (number of previous claims)",
            "Vehicle History (e.g., accidents, repairs)"
        ],
        "Health": [
            "Age", "Pre-existing Conditions", "Smoking Status", "Height (cm)", "Weight (kg)", 
            "Medical History (e.g., chronic diseases)", "Claim History (number of previous claims)"
        ],
        "Home": [
            "Property Value", "Property Address", "Home Age", "Security Features", "Square Footage", 
            "Claim History (number of previous claims)", "Personal Property Value"
        ],
        "Life": [
            "Age", "Occupation", "Annual Income", "Health Status", "Coverage Amount", 
            "Claim History (number of previous claims)"
        ]
    }
    
    # Form for specific fields and claims data
    with st.form("user_details_form"):
        st.subheader(f"{insurance_type} Insurance Details")
        user_data = {}
        for field in required_fields[insurance_type]:
            if field in ["Age", "Annual Mileage", "Height (cm)", "Weight (kg)", "Property Value", 
                         "Home Age", "Square Footage", "Annual Income", "Coverage Amount", 
                         "Driving History (years)", "Claim History (number of previous claims)"]:
                user_data[field] = st.number_input(field, min_value=0.0, step=1.0)
            else:
                user_data[field] = st.text_input(field)
        
        # Claims data (optional)
        st.subheader("Claims Data (if applicable)")
        claim_number = st.text_input("Claim Number")
        claim_type = st.text_input("Claim Type (e.g., accident, theft)")
        claim_date = st.date_input("Claim Date")
        loss_severity = st.number_input("Loss Severity (amount)", min_value=0.0, step=100.0)
        repair_costs = st.number_input("Repair or Replacement Costs", min_value=0.0, step=100.0)
        medical_expenses = st.number_input("Medical Expenses (if applicable)", min_value=0.0, step=100.0)
        
        # Store claims data
        claims_data = {
            "Claim Number": claim_number,
            "Claim Type": claim_type,
            "Claim Date": claim_date,
            "Loss Severity": loss_severity,
            "Repair or Replacement Costs": repair_costs,
            "Medical Expenses": medical_expenses
        }
        
        # File uploader for policy document
        policy_doc = st.file_uploader("Upload Policy Document", type=['pdf', 'doc', 'docx'])
        
        submitted = st.form_submit_button("Analyze Claims & Calculate Premium")
        
    if submitted:
        with st.spinner("Processing your data..."):
            # Merge all data: common, specific, and claims
            all_data = {**common_data, **user_data, **claims_data}
            
            # Process the uploaded document (placeholder until implemented)
            doc_content = ""  # Replace with process_doc(policy_doc, policy_doc.type) when available
            
            # Get analysis from Ollama
            text_placeholder = st.empty()
            response_text = ""
            for chunk in chat_with_llama(cq(insurance_type, all_data, doc_content)):
                response_text += chunk  # Append each chunk to the full response
                text_placeholder.write(response_text, unsafe_allow_html=True)  # Update progressively
            
            # Download button for PDF
            st.download_button(
                label="📥 Download Analysis Report",
                data=markdown_to_pdf(response_text),  # Assuming this function converts the response to PDF
                file_name=f"Insurance_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )                
           
def upload_or_delete_documents():
    """Function to handle the Upload Documents and Delete Vectors pages."""
    # Create two tabs
    upload_tab, delete_tab = st.tabs(["📤 Upload Documents", "🗑️ Delete Vectors"])

    # --- Upload Documents Tab ---
    st.sidebar.write("# Existing Uploaded Files:")
# Display existing uploaded files from JSON
    json_data = load_json()
    
# Display existing uploaded files from JSON
    if json_data:
        hoverable_files = []
        for filename, info in json_data.items():
            # Format metadata for the tooltip
            metadata = f"Uploaded: {info['upload_time']}, Chunks: {info['chunk_count']}, Collection: {info['collection_name']}"
            # Create HTML for each file: bold filename with hoverable tooltip
            hoverable_files.append(
                f"<div><span title='{metadata}' style='cursor:pointer;'>{filename}</span></div>"
            )
        # Join all file entries with newlines for separate lines
        files_html = "\n".join(hoverable_files)
        st.sidebar.markdown(f"{files_html}", unsafe_allow_html=True)
    else:
        st.sidebar.info("No files uploaded yet.")
    with upload_tab:
        st.header("Upload Documents")
        st.write("*Upload your insurance-related documents to fine-tune the AI chatbot.*")
        
        # Placeholder for feedback
        placeholder1 = st.empty()
        placeholder2 = st.empty()

        # File uploader in sidebar (scoped to upload tab)
        uploaded_files = st.file_uploader(
            "Upload a file",
            type=["txt", "pdf", "docx"],
            label_visibility="collapsed",
            accept_multiple_files=True,
            key="upload_tab_uploader"
        )

          # Clear the placeholder after displaying

        if st.button("Upload Files", key="upload_button"):
            if not uploaded_files:
                placeholder2.error("No files selected for upload.")
            else:
                counter = 0
                progress = st.progress(0)
                for i, uploaded_file in enumerate(uploaded_files):
                # for uploaded_file in uploaded_files:
                    placeholder1.write(f"- {uploaded_file.name}")
                    time.sleep(0.2)

                    doc = process_doc(uploaded_file, uploaded_file.type)
                    total_chunks = 0
                    if doc[0]:
                        counter += 1
                        placeholder1.success(f"Processed: {uploaded_file.name}")
                        for page in doc[1]:
                            result = westore(page["text"], page["page_number"], uploaded_file.name)
                            if result is not None and isinstance(result, tuple) and len(result) == 2:
                                flag, chunk_count = result
                            else:
                                flag, chunk_count = False, 0
                            if flag:
                                # Extract chunk count from message, e.g., "Successfully imported 5 chunks..."
                                total_chunks += int(chunk_count) if isinstance(chunk_count, (int, str)) and str(chunk_count).isdigit() else 0
                            else:
                                placeholder2.error(f"Error storing {uploaded_file.name}: {chunk_count}")
                        if total_chunks > 0:
                            # Update JSON with successful upload
                            add_file_to_json(uploaded_file.name, total_chunks, collection_name="insurance_data")
                            placeholder2.success(f"Uploaded {total_chunks} chunks from {uploaded_file.name} to vector database")
                        time.sleep(0.5)
                    else:
                        placeholder1.error(f"Error processing {uploaded_file.name}: {doc[1]}")
                    progress.progress((i + 1) / len(uploaded_files))


                if counter == len(uploaded_files):
                    placeholder2.success("Processed all uploaded files successfully!")

    # --- Delete Vectors Tab ---
    with delete_tab:
        st.header("Delete Vectors")
        st.write("*Delete specific vectors or collections from the vector database.*")
        
        # Placeholder for feedback
        placeholder3 = st.empty()

        # Deletion type selection
        delete_option = st.selectbox(
            "Select deletion type",
            ["Delete All", "UUID", "Chunk ID", "Filename", "Collection"],
            help="Choose what to delete from the vector database."
        )

        # Input fields based on deletion type
        delete_input = None
        collection_name = "insurance_data"  # Default collection name

        if delete_option == "UUID":
            delete_input = st.text_input("Enter UUID", key="uuid_input")
        elif delete_option == "Chunk ID":
            delete_input = st.text_input("Enter Chunk ID", key="chunk_id_input")
        elif delete_option == "Filename":
            delete_input = st.text_input("Enter Filename", key="filename_input")
        elif delete_option == "Collection":
            collection_name = st.text_input("Enter Collection Name", value="insurance_data", key="collection_input")

        if st.button("Delete", key="delete_button"):
            if delete_option != "Delete All" and delete_option != "Collection" and not delete_input:
                placeholder3.error("Please provide an input for deletion.")
            else:
                try:
                    # Map deletion options to wedel parameters
                    if delete_option == "Delete All":
                        flag, message = wedel(collection_name=collection_name)
                        if flag:
                            clear_collection_from_json(collection_name)
                    elif delete_option == "UUID":
                        flag, message = wedel(uuid_to_delete=delete_input, collection_name=collection_name)
                    elif delete_option == "Chunk ID":
                        flag, message = wedel(chunk_id=delete_input, collection_name=collection_name)
                    elif delete_option == "Filename":
                        flag, message = wedel(filename=delete_input, collection_name=collection_name)
                        if flag:
                            remove_file_from_json(delete_input)
                    elif delete_option == "Collection":
                        flag, message = wedel(collection_name=collection_name)
                        if flag:
                            clear_collection_from_json(collection_name)


                    if flag:
                        placeholder3.success(message)
                    else:
                        placeholder3.error(message)
                except Exception as e:
                    placeholder3.error(f"Deletion failed: {str(e)}")

def about_page():
    """Function to handle the About page."""
    st.title("ℹ️ About Our Insurance AI Assistant")
    
    # Main description with styling
    st.markdown("""
    
    ### 👋 Welcome to the AI-Powered Insurance Chatbot!
    Your intelligent companion for all insurance-related needs.
 
    """, unsafe_allow_html=True)

    # Key Features
    st.markdown("### 🌟 Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        * 🤖 **AI Chatbot**
            * 24/7 instant responses
            * Natural conversation flow
            * Personalized assistance
        
        * 📊 **Claims Analysis**
            * Detailed claims processing
            * Status tracking
            * Risk assessment
        """)
        
    with col2:
        st.markdown("""
        * 💰 **Premium Calculator**
            * Instant premium estimates
            * Multiple coverage options
            * Comparative analysis
            
        * 📄 **Document Management**
            * Secure file upload
            * Multi-format support
            * Automated processing
        """)

    # Technology Stack
    st.markdown("""
    ### 🛠️ Technology Stack
    
        - 🧠 Advanced LLM Integration
        - 🔄 Real-time Processing
        - 🔒 Secure Authentication
        - 💾 Vector Database Storage
        - 🌐 Streamlit Web Interface
    
    """, unsafe_allow_html=True)

    # Benefits
    st.markdown("### 💫 Benefits")
    st.markdown("""
    * ⚡ **Instant Support**: Get immediate answers to your insurance queries
    * 📱 **Accessibility**: Available 24/7 through web interface
    * 🎯 **Accuracy**: Powered by advanced AI for precise information
    * 🔐 **Security**: Your data is protected with secure authentication
    * 📈 **Efficiency**: Streamlined processes for claims and premium calculations
    """)

    # Dummy Contact Information
    st.markdown("""
    ### 📞 Need Help?
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
        * 📧 Email: support@insuranceai.com
        * 🌐 Website: www.insuranceai.com
        * 📱 Phone: 1-800-INS-CHAT
    </div>
    """, unsafe_allow_html=True)

    # Version Information
    st.markdown("""
    ---
    <div style='text-align: center; font-size: 0.8em;'>
        Version 1.0.0 | © 2024 Insurance AI Assistant | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)

def main_page():
    st.markdown(
        """
        <style>
        .logout-button {
            position: absolute;
            top: -30px;
            right: -85px;
        }
        </style>
        <div class="logout-button">
            <form action="/" method="get">
                <button style="background-color: #f44336; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;" type="submit">Logout</button>
            </form>
        </div>
        """,
        unsafe_allow_html=True
    )

     
    st.sidebar.header("User Options")
    option = st.sidebar.selectbox("Select an option", ["Chat with AI", "Upload/Delete Documents", "Claims Analysis and premium calculator","About"])  
    
    # Route to the appropriate function based on the selected option
    if option == "Chat with AI":
        chat_bot()
        if st.session_state["chat_history"]:
            transcript = "\n".join(
                f"{message['role'].capitalize()}: {message['content'].split('\n\n---\n')[0] if '\n\n---\n' in message['content'] else message['content']}"
                for message in st.session_state["chat_history"]
            )
            st.sidebar.download_button(
                label="📥 Download Chat Transcript",
                data=transcript,
                file_name="chat_transcript.txt",
                mime="text/plain",
            )


    elif option == "Claims Analysis and premium calculator":
        claims_analysis_and_premium_calculator()
        # claims_and_premium_calculator()

    elif option == "Upload/Delete Documents":
        upload_or_delete_documents()

    elif option == "About":
        about_page()

if __name__ == "__main__": 
    if st.session_state['logged_in']:
        main_page()  # Show the main page if logged in
    else:
        login_page()