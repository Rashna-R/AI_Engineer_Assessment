
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = os.getenv("GROQ_MODEL")

if not MODEL_NAME:
    MODEL_NAME = "llama-3.3-70b-versatile"


def ask_llm(user_query, data_result):
    prompt = f"""
You are a customer support ticket analytics assistant.

User question:
{user_query}

Actual result calculated from the customer support ticket dataset:
{data_result}

Instructions:
- Answer using ONLY the actual result provided.
- Do not invent or change numbers.
- Give a direct and concise answer.
- Keep the response professional.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You answer customer support analytics questions using provided dataset results."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def detect_intent(user_query):
    prompt = f"""
Classify this customer support analytics question into exactly ONE intent:

- count
- agent
- anomaly
- filtered_tickets
- average_rating
- unknown

User question:
{user_query}

Return ONLY the intent name.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You classify customer support analytics questions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()
