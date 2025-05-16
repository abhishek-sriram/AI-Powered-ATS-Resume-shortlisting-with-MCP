# import google.generativeai as genai

# API_KEY = "AIzaSyDvVl-2A0DmzniL0bLP1h7ovaPlKEfSnu0"
# genai.configure(api_key=API_KEY)

# model = genai.GenerativeModel("gemini-1.5-pro")

# try:
#     response = model.generate_content("Hello, world!")
#     print(response.text)
# except Exception as e:
#     print("Error:", e)

import requests

GROQ_API_KEY = "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"

def build_context_blocks(code_or_prompt: str):
    return [
        ]

def call_groq_with_context(prompt: str, context_blocks: list):
    context_string = "\n\n".join(
        f"[{block['type'].upper()}]\n{block['content']}" for block in context_blocks
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful Python code assistant. Use the context blocks to explain bugs, suggest fixes, and recommend libraries."
            )
        },
        {
            "role": "user",
            "content": f"{context_string}\n\n{prompt}"
        }
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",  # ✅ New working model
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("Groq API Error:", response.status_code, response.text)
        raise Exception("Groq API call failed")

    return response.json()["choices"][0]["message"]["content"]


def mcp_query(user_input: str):
    context = build_context_blocks(user_input)
    return call_groq_with_context(user_input, context)

if __name__ == "__main__":
    user_input = "What is the difference between a list and a tuple in Python?"
    response = mcp_query(user_input)
    print("Response from Groq API:\n", response)