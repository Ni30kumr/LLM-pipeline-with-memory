import streamlit as st
import requests

st.title("LLM-based RAG Search")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["assistant"])

# Input for user query
query = st.chat_input("Enter your query:")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    # Add user query to chat history
    st.session_state.chat_history.append({"user": query, "assistant": ""})

    try:
        # Make the POST request to Flask API
        response = requests.post(
            "http://localhost:5001/query",
            json={"query": query},
            timeout=15
        )

        if response.status_code == 200:
            answer = response.json().get('answer', "No answer received.")
            with st.chat_message("assistant"):
                st.markdown(answer)
            # Update the last assistant message in chat history
            st.session_state.chat_history[-1]["assistant"] = answer
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the Flask server: {e}")

