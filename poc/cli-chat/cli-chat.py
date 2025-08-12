# /// script
# requires-python = "==3.12"
# dependencies = ["google-genai>=1.29.0"]
# ///

import asyncio
import os
from google import genai


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    print("Please set it using: export GEMINI_API_KEY='YOUR_API_KEY'")
    assert (
        False
    ), "Error: GEMINI_API_KEY environment variable not set.\nPlease set it using: `export GEMINI_API_KEY='YOUR_API_KEY'`."


async def chat_with_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    chat = client.chats.create(model="gemini-2.5-flash")

    # The chat object will maintain the history
    chat.send_message("I have 2 dogs in my house.")
    chat.send_message("How many paws are in my house?")

    print("=== Printing the whold history (including responses). ===")
    for message in chat.get_history():
        print(f"Role - {message.role}: ", message.parts[0].text, "\n-----------------")


if __name__ == "__main__":
    asyncio.run(chat_with_gemini())
