# CapstoneProjectGPE
A web-based healthcare assistant (Flask + Gemini) for initial symptom triage. The UI stores chat history locally in the browser, supports both English and Indonesian, and uses a modular prompt system (RTCFC) to ensure consistency and safety.

## Features

* Modern chat UI with local conversation history (localStorage)
* English and Indonesian language support
* RTCFC-based modular prompting with safety constraints
* Simple chat endpoint powered by Gemini

## Prerequisites

* Python 3.10+
* Gemini API key

## Environment Setup

1. Create a virtual environment (optional).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the environment variable:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Or create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Project Structure

```text
.
├─ app.py
├─ requirements.txt
├─ static/
│  ├─ script.js
│  └─ style.css
├─ templates/
│  └─ index.html
├─ prompts/
│  ├─ 00_system/
│  ├─ 10_tasks/
│  ├─ 20_formats/
│  ├─ 30_examples/
│  └─ 40_experiments/
├─ prompts_id/
│  ├─ 00_system/
│  ├─ 10_tasks/
│  ├─ 20_formats/
│  ├─ 30_examples/
│  └─ 40_experiments/
└─ docs/
   ├─ dokumentasi-proyek.md
   └─ plan.md
```

## Prompt Configuration

The default prompt pipeline is defined in `app.py` through the `build_system_prompt()` function.

Default component order:

1. `rtcfc_base.txt`
2. `safety_constraints.txt`
3. `disclaimer.txt`
4. `symptom_triage.txt`
5. `output_template.txt`
6. `few_shot_qa.txt`

The Indonesian version is located in the `prompts_id/` directory with the same structure.

## Notes

* Chat history is stored in the browser, not on the server.
* The `/chat` endpoint ignores client-side history (the server starts a new chat session for each request).
