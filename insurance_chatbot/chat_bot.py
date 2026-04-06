import streamlit as st
from agent import chat_with_llama, chat_with_llama_direct
from prompt import past_or_present as pop

if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

# Display existing chat history
for message in st.session_state["chat_history"]:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"],unsafe_allow_html=True)

# Ensure chat history does not exceed 10 messages


# Chat input for user messages
prompt = st.chat_input(placeholder="Ask about insurance, claims, or premiums...")
if prompt:
    # Add user message to chat history
    st.chat_message("user").write(prompt)
    # Create a placeholder for the assistant's response
    assistant_message = st.chat_message("assistant")
    response_placeholder = assistant_message.empty()

    # Stream the response from the Llama model
    response_text = ""  # To store the full response
    summary=""
    # if "chat_history" in st.session_state: 
    #     summary = chat_with_llama_direct(sumcon(st.session_state["chat_history"]))
    #     print(summary)

    # print(query)
    st.session_state["chat_history"].append({"role": "user", "content": prompt})

    for chunk in chat_with_llama(prompt):
         response_text += chunk  # Append each chunk to the full response
         response_placeholder.write(response_text)  # Update the placeholder progressively
 # Append each chunk to the full response
  
    # Format and append the file names to the response
    
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
    st.session_state["chat_history"].append({"role": "assistant", "content": response_text })
