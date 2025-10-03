import os
from dotenv import load_dotenv
import google.genai as genai
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=api_key)

PROMPT_TEMPLATE = """
Read the text below and produce a JSON object with the following fields:

- title: Write a short, human-friendly title (5–12 words) that captures the main idea. Do not just copy the opening line.
- summary: Write a clear 1–2 sentence summary of the text.
- topics: Pick exactly 3 short topic keywords (each 1–3 words).
- sentiment: Choose one word: "positive", "neutral", or "negative" to describe the overall tone.

Text:
\"\"\"{text}\"\"\"

Return only the JSON object. Do not include explanations, formatting, or markdown.
"""


def analyze_with_llm(text: str):
    try:
        prompt = PROMPT_TEMPLATE.format(text=text)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()
        print("Raw LLM response:", raw_text) 

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json\n", "", 1).replace("json", "", 1).strip()

        return json.loads(raw_text)

    except Exception as e:
        raise RuntimeError(f"LLM error: {str(e)}")
