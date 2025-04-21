# 🏗️ Project Architecture — YouTube Transcript & Summary Generator

This document outlines the complete technical architecture of the project, including its backend/frontend structure, AI engine integration, token-based text chunking system, dependency injection mechanism, and test strategy.

---

## ⚙️ Overview

The application extracts transcripts from YouTube videos and uses an AI engine (OpenAI or Ollama) to generate structured summaries with customizable formats and styles.

---

## 🧱 Application Structure

```bash
.
├── app.py                   # Flask entrypoint
├── routes/                 # Flask routes (summary, transcript)
├── services/               # Business logic (AI clients, transcript, prompt, splitters)
├── utils/                  # Shared helpers (config, logger, decorators, sanitizer)
├── templates/              # HTML (Jinja2 templates)
├── static/                 # JS, CSS, favicon
├── prompts/                # Prompt templates (externalized)
├── tests/                  # Unit + integration tests (Pytest + Jest)
├── requirements.txt
└── run.sh
```

---

## 🧠 AI Engine Integration

Supported AI engines:
- `OpenAI` (GPT-4o by default via API)
- `Ollama` (local models via local endpoint)

Users can:
- Use the platform’s default OpenAI key
- Provide their own OpenAI API key + endpoint

Selection is handled via a radio input and passed to the backend with each request.

---

## 🪄 Summary Generation Flow

1. **User submits a YouTube URL + customization options**
2. **Transcript extraction** via YouTube API
3. **Transcript is split into token-safe chunks** using `tiktoken`
4. First chunk → `build_initial_prompt()`  
   Other chunks → `build_update_prompt(previous_summary)`
5. Each chunk is sent to the LLM client (OpenAI/Ollama)
6. Each partial summary is chained with the previous one
7. Final result is converted to HTML using `markdown.markdown()` and returned

---

## ✂️ Token-Based Text Splitting

- Transcript is split by sentence.
- Each chunk is encoded with `tiktoken` and must remain under `MAX_TOKENS`.
- If a single sentence exceeds the limit, it is isolated into its own chunk.

```python
split_transcript_by_tokens(text, max_tokens=10000, model="gpt-3.5-turbo")
```

---

## 🧩 Dependency Injection System

Decorators used:
- `@inject_logger`
- `@inject_config`
- `@inject_dependencies` (for both)

This allows services and routes to receive pre-injected `config` and `logger` objects. No global import of `config` or `get_logger()` in logic functions = more modular and testable.

---

## 🧪 Testing Strategy

### Backend (Python – Pytest)

- Unit tests for all services: `youtube_transcript`, `ollama_client`, `openai_client`, `splitter`, `prompt_builder`
- Integration tests for Flask routes: `summarize`, `get_transcript_only`

### Frontend (JavaScript – Jest + jsdom)

- DOM logic (copy, download, loading animation, clipboard)
- Uses `@jest-environment jsdom` to simulate browser environment
- HTML template is loaded dynamically before each test

```bash
cd tests/test_frontend
npm test
```

---

## 🔁 CI/CD

CI is powered by **GitHub Actions**:
- Python tests (pytest) and JS tests (Jest) run on each push and pull request
- Node.js and Python environments are both set up and cached
- Workflow: `.github/workflows/test.yml`

---

## 🐳 Docker (Coming soon)

A `Dockerfile` and `docker-compose.yml` are planned to encapsulate:
- Flask server
- Ollama service
- Node.js build for JS tests (optional)

---

## 🧩 Modularity

- Prompt logic is externalized in `/prompts/`
- Config is isolated and validated using `pydantic-settings`
- Logger is injectable for mocking
- Backend is test-friendly and ready for scaling (even without microservices)

---

## ✅ Notes

- App is local-first, with future deployment to Hostinger VPS
- User API key support and language autodetection are in production
- No database, no persistent storage: pure stateless generation