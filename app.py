import streamlit as st
import requests

# Streamlit app configuration
st.set_page_config(page_title="Slickonveksi Chatbot", page_icon="🤖", layout="wide")

# Title and header
st.title("🤖 Slickonveksi Chatbot")
st.subheader("Your virtual assistant for Slickonveksi!")

# Sidebar
with st.sidebar:
    st.markdown("### Slickonveksi Chatbot")
    st.markdown(
        "Chatbot ini merupakan chatbot perusahaan konveksi Slickonveksi untuk membantu menjawab pertanyaan pelanggan."
    )
    st.markdown("### Contact Us")
    st.markdown("Have feedback? Contact us!")

# Placeholder for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# API endpoint for the Rasa chatbot
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

# Create a container for displaying messages
chat_container = st.container()

# Input box container
input_container = st.container()

# Function to display chat messages with custom CSS (padding added)
def display_messages():
    with chat_container:
        for message in st.session_state.messages:
            if message["is_user"]:
                st.markdown(f'''
                    <div style="text-align: right; color: #0078D4; padding: 10px; margin-bottom: 10px; border-radius: 8px;">
                        <strong>🧑 You:</strong> {message["text"]}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div style="text-align: left; color: #4CAF50; padding: 10px; margin-bottom: 10px; border-radius: 8px;">
                        <strong>🤖 Bot:</strong> {message["text"]}
                    </div>
                ''', unsafe_allow_html=True)

# Display chat messages
display_messages()

# Input box for user to type a message
with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here", key="input")
        submit_button = st.form_submit_button(label="Send")

    # Handle user input
    if submit_button and user_input:
        # Clear the previous chat history (optional)
        st.session_state.messages.clear()

        # Add user message to the chat history
        st.session_state.messages.append({"is_user": True, "text": user_input})

        # Send user input to Rasa server
        try:
            response = requests.post(
                RASA_API_URL,
                json={"sender": "user", "message": user_input},
                timeout=10,
            )
            response.raise_for_status()
            bot_responses = response.json()

            # Add bot responses to the chat history
            for bot_message in bot_responses:
                st.session_state.messages.append(
                    {"is_user": False, "text": bot_message.get("text", "I didn't understand that.")}
                )
        except requests.exceptions.RequestException:
            st.error("Error connecting to the Rasa server. Please ensure it's running.")

        # Refresh the chat messages
        display_messages()
