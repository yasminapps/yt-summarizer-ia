# 🧠 Project Architecture - yt-summarizer-ia

## 📁 Project Structure

yt-summarizer-ia/
│
├── app.py                       # Entry point of the Flask application
├── config.py                    # Optional config file
├── requirements.txt             # Python dependencies
├── CONTRIBUTING.md              # Contribution guidelines
├── README.md                    # Project overview and usage
│
├── templates/
│   └── index.html               # Main HTML interface
│
├── static/
│   ├── style.css                # CSS styles
│   └── script.js                # Frontend interactivity (toggle, auto-language)
│
├── routes/
│   └── summarize.py             # POST route to handle summarization
│
├── services/
│   ├── openai_client.py         # Calls OpenAI API (remote summarization)
│   ├── ollama_client.py         # Calls local Ollama server (offline summarization)
│   ├── youtube_transcript.py    # Extracts YouTube transcript from video URL
│   └── ia_client_factory.py     # Chooses LLM engine (OpenAI vs Ollama)
│
├── utils/
│   ├── formatter.py             # Cleans up transcript text
│   ├── logger.py                # (Optional) logging utility
│   └── decorators.py            # (Optional) decorators
│
├── tests/
│   └── test_api.py              # Unit test for API behavior
│
└── docs/
└── architecture.md          # Current documentation file


---

## 🧩 Core Components

| Component              | Description                                                            |
|------------------------|------------------------------------------------------------------------|
| `Flask`                | Lightweight web server for routing and request handling                |
| `YouTubeTranscriptAPI` | Extracts video subtitles automatically                                 |
| `Ollama`               | Local LLM engine (e.g. LLaMA3) without Internet access                 |
| `OpenAI API`           | Remote LLM engine (GPT-3.5/4), requires API key and endpoint           |
| `dotenv`               | Loads environment variables from `.env` securely                      |
| `HTML/CSS/JS`          | User interface with multi-language and interactive elements            |

---

## 🔁 Execution Workflow

1. User submits a YouTube URL, chooses the LLM engine, summary type, target language, and detail level.
2. The backend fetches the video transcript.
3. A tailored prompt is generated based on user inputs.
4. The IA engine is selected via the `ia_client_factory`.
5. The summary is generated using OpenAI or Ollama.
6. The result (summary + optional token usage) is returned to the frontend.

---

## 🧱 Design Patterns & Best Practices

- **Factory Pattern**: `get_llm_client()` dynamically selects the correct LLM engine.
- **Separation of Concerns**: Clear separation between logic (`services`), interface (`routes`, `templates`), and utilities (`utils`).
- **Environment Safety**: `.env` file is used via `python-dotenv` to protect sensitive credentials.
- **Frontend Modularity**: JavaScript and CSS are in separate files for maintainability.
- **Multilingual UX**: Auto-detects browser language and allows any language via `datalist`.
- **Open Source Ready**: Standard GitHub layout, documentation folder, clear modular structure.

---

## 📌 Notes

- The project is designed for easy contribution, modular evolution, and eventual deployment.
- Future enhancements include automatic language detection, caching, user auth, and UI refinement.
