# 🎥 yt-summarizer-ia

An AI-powered summarizer for YouTube videos — using either a local LLM (Ollama) or a remote model (OpenAI).  
It extracts the transcript from a video, generates a custom prompt, and returns a clean summary in your preferred language and format.

---

## 🚀 Features

- Summarize any public YouTube video.
- Choose between **OpenAI** and **Ollama** as the LLM backend.
- Control the **type**, **language**, and **detail level** of the summary.
- Automatic browser language detection.
- Secure use of OpenAI API (key not stored).
- Works offline with local LLMs (via Ollama).

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/yt-summarizer-ia.git
cd yt-summarizer-ia
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv yt_env
source yt_env/bin/activate  # or use `.\yt_env\Scriptsctivate` on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Create a `.env` file

```env
OPENAI_API_KEY=your-key-here
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
```

---

## ▶️ Run the app

```bash
python app.py
```

Then go to [http://localhost:5002](http://localhost:5002)

---

## 📦 Project structure

See [`docs/architecture.md`](docs/architecture.md) for detailed component breakdown.

---

## ✅ Example usage

1. Paste any public YouTube URL.
2. Choose your AI model (OpenAI or Ollama).
3. Select the type of summary:
   - **🧰 Tools & Methods**
   - **📖 Full Summary**
   - **💡 Key Learnings**
4. Choose the language and detail level.
5. Click **"Summarize"** and get your result.

---

## 🧪 Tests

Run the API test with:

```bash
pytest tests/test_api.py
```

---

## 🤝 Contributing

Feel free to open issues or submit pull requests.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md) for more details.

---

## 📘 License

MIT License. See `LICENSE` file.
