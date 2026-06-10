from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Peringatan: File prompt tidak ditemukan: {file_path}")
        return ""

DEFAULT_PROMPT = "You are a helpful assistant."

PROMPT_COMPONENTS = {
    "en": [
        "prompts/00_system/rtcfc_base.txt",
        "prompts/00_system/safety_constraints.txt",
        "prompts/00_system/disclaimer.txt",
        "prompts/10_tasks/symptom_triage.txt",
        "prompts/20_formats/output_template.txt",
        "prompts/30_examples/few_shot_qa.txt",
    ],
    "id": [
        "prompts_id/00_system/rtcfc_base.txt",
        "prompts_id/00_system/safety_constraints.txt",
        "prompts_id/00_system/disclaimer.txt",
        "prompts_id/10_tasks/symptom_triage.txt",
        "prompts_id/20_formats/output_template.txt",
        "#prompts_id/30_examples/few_shot_qa.txt",
    ],
}

def build_system_prompt(language):
    paths = PROMPT_COMPONENTS.get(language, PROMPT_COMPONENTS["en"])
    parts = [load_prompt_file(path) for path in paths]
    parts = [part for part in parts if part]
    return "\n\n".join(parts).strip()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        language = (data.get("language") or "en").lower()
        history = data.get("history") or []
        

        if not user_message:
            error_message = (
                "Pesan tidak boleh kosong." if language == "id" else "Message cannot be empty."
            )
            return jsonify({"error": error_message}), 400

        system_prompt = build_system_prompt(language) or DEFAULT_PROMPT

        # Use a small, recent window of history to save tokens.
        max_turns = 6
        trimmed_history = history[-max_turns:]

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
        )
        chat_session = model.start_chat(history=trimmed_history)

        
        response = chat_session.send_message(user_message)

        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error during chat: {e}")
        error_message = (
            "Maaf, terjadi masalah di server." if data.get("language") == "id" else "Sorry, a server error occurred."
        )
        return jsonify({"error": error_message}), 500


if __name__ == "__main__":
    app.run(debug=True)