# 📑 API Reference – YouTube Transcript & Summary Generator

This document describes the available API endpoints used in the Flask backend.

---

## 🔁 POST `/summarize`

Generates a structured AI summary from a YouTube video link and user preferences.

### 📥 Request (Form Data)

| Field                 | Type    | Required | Description                                           |
|----------------------|---------|----------|-------------------------------------------------------|
| `youtube_url`        | string  | ✅       | YouTube video link                                   |
| `engine`             | string  | ❌       | AI engine: `openai-default` (default), `openai-user`, `ollama` |
| `api_key`            | string  | ❌       | User’s OpenAI API key (used only if `engine = openai-user`) |
| `api_url`            | string  | ❌       | Custom API endpoint (for `openai-user`)              |
| `summary_type`       | string  | ❌       | `full`, `tools`, `insights`                          |
| `language`           | string  | ❌       | Output language (`en`, `fr`, etc.)                   |
| `detail_level`       | string  | ❌       | `short`, `medium`, `detailed`                        |
| `style`              | string  | ❌       | `mixed`, `text_only`, `bullet_points`                |
| `add_emojis`         | string  | ❌       | `yes` or `no`                                         |
| `add_tables`         | string  | ❌       | `yes` or `no`                                         |
| `specific_instructions` | string | ❌     | Freeform instructions added to the prompt            |

---

### 📤 Response (JSON)

| Field            | Type    | Description                                 |
|------------------|---------|---------------------------------------------|
| `summary`        | string  | HTML-formatted AI summary                   |
| `transcript`     | string  | Clean transcript (if available)             |
| `tokens`         | object  | Token usage metadata from the API          |
| `execution_time` | float   | Time taken to process request (in seconds) |

---

### ⚠️ Possible Errors

| Status | Message                                                     |
|--------|-------------------------------------------------------------|
| 400    | "Invalid YouTube URL" or transcript not available           |
| 500    | "Error during summarization process"                        |

---

## 🔁 POST `/transcript`

Returns only the transcript of a given YouTube video.

### 📥 Request (Form Data)

| Field           | Type   | Required | Description             |
|----------------|--------|----------|-------------------------|
| `youtube_url`  | string | ✅       | Link to YouTube video   |

---

### 📤 Response (JSON)

| Field        | Type    | Description                     |
|--------------|---------|---------------------------------|
| `transcript` | string  | Cleaned transcript text         |

---

### ⚠️ Possible Errors

| Status | Message                                           |
|--------|---------------------------------------------------|
| 400    | "Invalid YouTube URL" or extraction failure       |
| 500    | "Error during transcript extraction"              |

---

## 🧠 Internals (Used by summarize route)

- `get_transcript_text(youtube_url)` → Extracts transcript (YouTube API)
- `split_transcript_by_tokens(text)` → Token-safe chunking
- `build_initial_prompt(chunk, user_choices)`
- `build_update_prompt(chunk, prev_summary, idx, user_choices)`
- `get_llm_client(engine, api_key, api_url)` → Returns callable OpenAI/Ollama wrapper
- `call_openai_llm(prompt, ...)` → Handles OpenAI chat completions
- `call_ollama_llm(prompt)` → Handles Ollama local completions

---

## ✅ Supported Engines

- `openai-default` → Uses backend’s default OpenAI key
- `openai-user` → Uses user-provided OpenAI key
- `ollama` → Uses local Ollama engine

---

## 🔐 Security & Validation

- All input fields are sanitized and validated (`sanitize_form_data`)
- API keys are never logged or stored
- Requests are timed and logged using decorators

---

## 📦 Response Format

All responses are returned in JSON with appropriate HTTP status codes.