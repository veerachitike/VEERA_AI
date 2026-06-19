import time
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(prompt):

    try:

        start = time.time()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
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

        error = str(e)

        if "429" in error:

            print(
                "Gemini Quota Exceeded:",
                error
            )

            return (
                "I have reached my Gemini usage limit. "
                "Please try again later."
            )

        print(
            "Gemini Error:",
            error
        )

        return (
            "I am having trouble connecting to Gemini."
        )