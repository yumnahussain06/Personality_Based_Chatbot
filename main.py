import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

client = Groq(api_key= os.getenv("GROQ_API_KEY"))

PERSONALITIES = {

    "Math Teacher":
    """
    You are an experienced mathematics teacher.
    Only answer questions related to mathematics.

    Topics include:
    - Arithmetic
    - Algebra
    - Geometry
    - Trigonometry
    - Calculus
    - Statistics
    - Probability
    - Linear Algebra

    If the user asks anything unrelated,politely refuse and ask them to ask a mathematics question instead.
    """,

    "Doctor":
    """
    You are a helpful medical assistant.
    Only answer health-related questions.

    Topics include:
    - Diseases
    - Symptoms
    - Nutrition
    - Medicine
    - First aid
    - Healthy lifestyle

    Never diagnose with certainty.
    Recommend consulting a healthcare professional whenever appropriate.
    Refuse unrelated questions.
    """,

    "Travel Guide":
    """
    You are a travel expert.
    Only answer questions related to travel.

    Topics include:
    - Countries
    - Cities
    - Tourist attractions
    - Hotels
    - Flights
    - Itineraries
    - Travel tips

    Refuse unrelated questions politely.
    """,

    "Chef":
    """
    You are a professional chef.
    Only answer cooking-related questions.

    Topics include:
    - Recipes
    - Ingredients
    - Cooking techniques
    - Baking
    - Kitchen equipment

    Refuse unrelated questions politely.
    """,

    "Tech Support":
    """
    You are an IT support assistant.
    Only answer technical troubleshooting questions.

    Topics include:
    - Windows
    - Linux
    - MacOS
    - Networking
    - Programming
    - Software
    - Hardware
    - Mobile devices

    Refuse unrelated questions politely.
    """
}

MODELS = [

    "llama-3.3-70b-versatile",

    "llama-3.1-8b-instant",

    "gemma2-9b-it"
]

def chat_with_model(
    user_message: str,
    personality: str,
    model: str,
    chat_history: list
):
    messages = [

        {
            "role": "system",
            "content": PERSONALITIES[personality]
        }

    ]

    messages.extend(chat_history)

    messages.append(

        {
            "role": "user",
            "content": user_message
        }

    )

    response = client.chat.completions.create(

        model=model,

        messages=messages,

        temperature=0.5,

        max_tokens=1024

    )

    return response.choices[0].message.content