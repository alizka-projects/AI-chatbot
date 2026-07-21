import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("API_KEY"))

messages = [{
    "role":"system",
    "content":"You are a friendly AI assisstant"
}]

def chat_with_AI(user_message):
    messages.append(
        {"role": "user",
        "content": user_message}
        )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    bot_reply = response.choices[0].message.content
    messages.append(
        {"role": "assistant",
        "content": bot_reply}
        )
    return bot_reply