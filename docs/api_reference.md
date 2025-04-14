# 📘 API Reference – yt-summarizer-ia

This document provides technical reference for the internal logic and key functions of the project.

---

## 🔁 Main Endpoints

### `POST /summarize`
Summarizes a YouTube video transcript using an AI engine (OpenAI or Ollama).

**Request Parameters (form-data):**
| Field         | Type     | Description                                                   |
|---------------|----------|---------------------------------------------------------------|
| `youtube_url` | string   | Full YouTube video link (supports `youtube.com` and `youtu.be`) |
| `engine`      | string   | `"openai"` or `"ollama"`                                      |
| `api_key`     | string   | API key (required for OpenAI only)                            |
| `api_url`     | string   | API endpoint (required for OpenAI only)                       |
| `summary_type`| string   | `"full"`, `"tools"`, or `"key_learnings"`                    |
| `language`    | string   | Language code for the summary (e.g., `"en"`, `"fr"`, `"es"`)  |
| `detail_level`| string   | `"short"`, `"medium"`, or `"detailed"`                        |

**Response JSON:**
```json
{
  "summary": "Generated summary content...",
  "tokens": {
    "prompt_tokens": 123,
    "completion_tokens": 456,
    "total_tokens": 579
  }
}
```

---

## ⚙️ Main Functions

### `call_ollama_llm(prompt: str, model: str = "llama3", stream: bool = False) -> str`
Sends a prompt to the local Ollama instance and returns the response.

---

### `call_openai_llm(prompt: str, api_url: str, api_key: str, model: str = "gpt-3.5-turbo") -> dict`
Sends a prompt to the OpenAI-compatible API endpoint with authentication.

**Returns:**  
```python
{
  "response": "summary text",
  "tokens_used": {
    "prompt_tokens": ...,
    "completion_tokens": ...,
    ...
  }
}
```

---

### `get_llm_client(engine, api_url="", api_key="") -> Callable`
Factory function that returns the appropriate LLM client based on user selection.

- If `engine == "openai"` and both `api_url` and `api_key` are provided → returns a wrapper around `call_openai_llm`.
- Otherwise → defaults to `call_ollama_llm`.

---

### `get_transcript_text(video_url, languages=['fr', 'en']) -> str`
Extracts and formats the transcript of a YouTube video using `YouTubeTranscriptApi`.

---

### `clean_transcript(raw_text: str, max_length: int = 3000) -> str`
Cleans and trims the raw transcript:
- Removes extra whitespace, tags like `[MUSIC]`, etc.
- Truncates to a defined maximum number of characters.

---

## 📁 Related Files

| File                           | Role                                                       |
|--------------------------------|------------------------------------------------------------|
| `routes/summarize.py`          | Handles POST form submission and orchestrates the workflow |
| `services/openai_client.py`    | OpenAI API integration                                     |
| `services/ollama_client.py`    | Ollama (local LLM) integration                            |
| `services/youtube_transcript.py`| Extracts text from YouTube videos                         |
| `services/ia_client_factory.py`| Dynamic engine selector (OpenAI or Ollama)                |
| `utils/formatter.py`           | Cleans and formats transcript                             |

---

## 🧪 Testing

- You can test `call_openai_llm` or `call_ollama_llm` via the script `test_api.py`.
- Use `test-pointenv` for manual test input outside of the web interface.

---

📄 **Note:** This document is part of the `docs/` directory. It is intended for contributors and advanced users.
