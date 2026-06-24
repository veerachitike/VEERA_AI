import time
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_model():

    try:

        with open(
            "settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

        return settings.get(
            "model",
            "gemini-2.5-flash"
        )

    except Exception as e:

        print(
            "Settings Read Error:",
            e
        )

        return "gemini-2.5-flash"
    

def ask_ai(prompt):

    try:

        start = time.time()

        model_name = get_model()

        print(
            f"Using Model: {model_name}"
        )

        response = client.models.generate_content(
            model=model_name,
            contents=f"""
            Answer briefly in 3 sentences.
            Keep the answer under 80 words.

            Question:
            {prompt}
            """
        )

        end = time.time()

        print(
            f"Gemini response time: "
            f"{end - start:.2f} seconds"
        )

        if not response.text:

            return (
                "I could not generate a response."
            )

        return response.text.strip()

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e))
        print(str(e))
        print("==================================\n")

        error = str(e)

        if "503" in error:

            return (
                "Gemini servers are currently busy. "
                "Please try again in a few moments."
            )

        if "429" in error:

            return (
                "Gemini quota exceeded. "
                "Please try again later."
            )

        if "401" in error:

            return (
                "Gemini API key is invalid."
            )

        return (
            f"Gemini Error: {error[:200]}"
        )