from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Send a question to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain Python in simple words."
)

# Display AI response
print(response.text)