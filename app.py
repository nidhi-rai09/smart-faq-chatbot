# ---------------------------------
# SMART FAQ CHATBOT
# ---------------------------------

# Import required libraries
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


# ---------------------------------
# STEP 1: LOAD API KEY
# ---------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found! Please check your .env file.")
    exit()

# Connect to Gemini
client = genai.Client(api_key=api_key)


# ---------------------------------
# STEP 2: CREATE CHAT SESSION
# ---------------------------------

chat = client.chats.create(
    model="gemini-3.5-flash-lite",

    config=types.GenerateContentConfig(
        system_instruction="""
        You are Smart FAQ Chatbot, a friendly college assistant.

        Follow these rules:
        1. Give simple and beginner-friendly answers.
        2. Keep answers short and clear.
        3. Explain technical terms with examples.
        4. Use bullet points whenever helpful.
        5. Understand follow-up questions using conversation context.
        6. Focus on educational and technical topics.
        7. Be polite and helpful.
        """
    )
)


# ---------------------------------
# STEP 3: CREATE FAQ DATABASE
# ---------------------------------

faq = {

    "what is python":
        "Python is a simple and popular programming language.",

    "tell me about python":
        "Python is a high-level programming language.",

    "explain python":
        "Python is a programming language known for its simple syntax.",

    "what is ai":
        "AI stands for Artificial Intelligence. It enables machines to perform tasks that normally require human intelligence.",

    "what is ml":
        "ML stands for Machine Learning. It allows computers to learn from data.",

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
# STEP 4: CHATBOT INTRODUCTION
# ---------------------------------

print("\n===================================")
print("       SMART FAQ CHATBOT")
print("===================================")

print("Hello! Welcome to Smart FAQ Chatbot.")
print("Ask me any educational question.")
print("Type 'exit' to close the chatbot.")
print("===================================\n")


# ---------------------------------
# STEP 5: CHATBOT MAIN LOOP
# ---------------------------------

while True:

    question = input("Ask a question: ")

    # Convert input into lowercase
    question = question.lower().strip()

    # Remove question mark
    question = question.replace("?", "")

    # Exit condition
    if question == "exit":
        print("\nThank you for using Smart FAQ Chatbot!")
        print("Goodbye!")
        break

    # Handle empty input
    if question == "":
        print("Please enter a question.\n")
        continue

    # ---------------------------------
    # STEP 6: CHECK FAQ DATABASE
    # ---------------------------------

    if question in faq:

        print("\nChatbot:", faq[question])

    # ---------------------------------
    # STEP 7: USE GEMINI FOR UNKNOWN QUESTIONS
    # ---------------------------------

    else:

        print("\nAsking Gemini AI...")

        try:

            response = chat.send_message(question)

            print("\nGemini:", response.text)

        except Exception as error:

            print("\nSorry! Gemini is temporarily unavailable.")
            print("Error type:", type(error).__name__)

    print("\n")