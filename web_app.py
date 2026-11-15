import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# ---------------------------------
# 1. Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Smart FAQ Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------
# 2. Load Gemini API Key
# ---------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# ---------------------------------
# 3. Create Gemini Client and Chat
# ---------------------------------

if "client" not in st.session_state:

    st.session_state.client = genai.Client(
        api_key=api_key
    )

if "chat" not in st.session_state:

    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="""
            You are Smart FAQ Chatbot, a friendly college assistant.

            Give simple, beginner-friendly and clear answers.
            Explain technical concepts with examples.
            Keep answers short and useful.
            """
        )
    )

chat = st.session_state.chat

# ---------------------------------
# 4. FAQ Database
# ---------------------------------

faq = {

    "what is python":
    "Python is a simple and popular programming language.",

    "what is ai":
    "AI stands for Artificial Intelligence. It enables machines to perform tasks that normally require human intelligence.",

    "what is ml":
    "ML stands for Machine Learning. It allows computers to learn from data.",

    "what is machine learning":
    "Machine Learning is a branch of AI that enables computers to learn from data and make predictions.",

    "explain machine learning":
    "Machine Learning is a branch of AI that enables computers to learn from data and make predictions.",

    "what is dsa":
    "DSA stands for Data Structures and Algorithms. It helps us organize data and solve problems efficiently.",

    "what is dbms":
    "DBMS stands for Database Management System. It is software used to store, manage and retrieve data.",

    "what is sql":
    "SQL stands for Structured Query Language. It is used to manage data in relational databases.",

    "what is cloud computing":
    "Cloud computing provides computing services such as storage and servers over the internet."
}

# ---------------------------------
# 5. Sidebar
# ---------------------------------

with st.sidebar:

    st.title("🤖 Smart FAQ")

    st.write("Your AI-powered college assistant!")

    st.divider()

    st.subheader("📚 Available Topics")

    st.write("📌 Python")
    st.write("📌 Artificial Intelligence")
    st.write("📌 Machine Learning")
    st.write("📌 Data Structures and Algorithms")
    st.write("📌 DBMS")
    st.write("📌 SQL")
    st.write("📌 Cloud Computing")

    st.divider()

    if st.button("🧹 Clear Chat", use_container_width=True):

        st.session_state.messages = []

        # Start a fresh Gemini conversation
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction="""
                You are Smart FAQ Chatbot, a friendly college assistant.
                Give simple, beginner-friendly and clear answers.
                Explain technical concepts with examples.
                Keep answers short and useful.
                """
            )
        )

        st.rerun()

# ---------------------------------
# 6. Chatbot Heading
# ---------------------------------

st.title("🤖 Smart FAQ Chatbot")

st.write(
    "Hello! Welcome to your AI-powered college assistant."
)

st.write(
    "Ask me questions about Python, AI, ML, DBMS and more!"
)

st.divider()

# ---------------------------------
# 7. Initialize Chat History
# ---------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# ---------------------------------
# 8. Quick Questions
# ---------------------------------

st.subheader("💡 Try asking:")

col1, col2 = st.columns(2)

with col1:

    if st.button("🐍 What is Python?", use_container_width=True):
        st.session_state.pending_question = "What is Python?"

    if st.button("🤖 What is AI?", use_container_width=True):
        st.session_state.pending_question = "What is AI?"

with col2:

    if st.button("🧠 What is Machine Learning?", use_container_width=True):
        st.session_state.pending_question = "What is Machine Learning?"

    if st.button("🗄️ What is DBMS?", use_container_width=True):
        st.session_state.pending_question = "What is DBMS?"

st.divider()

# ---------------------------------
# 9. Display Previous Messages
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------------
# 10. Get User Input
# ---------------------------------

question = st.chat_input("Type your question here...")

# Check whether a quick question was clicked
if "pending_question" in st.session_state:

    question = st.session_state.pop("pending_question")

# ---------------------------------
# 11. Generate Chatbot Response
# ---------------------------------

if question:

    # Display user question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking... 🤔"):

            try:

                # Clean the question
                clean_question = question.lower().strip()

                clean_question = clean_question.rstrip("?!.")

                # Check FAQ database first
                if clean_question in faq:

                    answer = faq[clean_question]

                    st.write("📚 Answer from FAQ Database")

                else:

                    # Use Gemini AI
                    st.write("🤖 Answer from Gemini AI")

                    response = st.session_state.chat.send_message(
                        question
                    )

                    answer = response.text

                # Display answer
                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error("Sorry! Something went wrong.")

                st.exception(error)