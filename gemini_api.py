import os
import json
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def interpret_mood_with_fallback(mood: str, max_keywords: int = 5):
    mood = (mood or "").strip()
    if not mood:
        return ("", "No mood provided")

    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            prompt = f"Extract {max_keywords} short keywords (comma-separated) for musical search: '{mood}'"
            model = genai.TextGenerationModel() if hasattr(genai, "TextGenerationModel") else None
            if model:
                resp = model.generate(prompt=prompt, max_output_tokens=100)
                text = resp.text if hasattr(resp, "text") else str(resp)
            else:
                resp = genai.generate_text(model="gemini-pro", prompt=prompt)
                text = resp.text
            keywords = text.splitlines()[0]
            summary = " ".join(text.splitlines()[1:]).strip() or "Interpreted mood keywords"
            return (keywords.strip(), summary.strip())
        except:
            pass

    tokens = mood.replace(",", " ").replace("/", " ").split()
    seen = []
    for t in tokens:
        w = t.strip().lower()
        if len(w) > 2 and w not in seen:
            seen.append(w)
    keywords = ", ".join(seen[:max_keywords])
    summary = f"Fallback keywords derived from input mood: {keywords}"
    return (keywords, summary)
