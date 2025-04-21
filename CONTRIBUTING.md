# 🤝 Contributing Guide

Thanks for your interest in contributing to **YouTube Transcript & Summary Generator**!

We welcome all kinds of contributions: bug reports, feature ideas, code improvements, UI tweaks, or documentation enhancements.

---

## 📦 Project Setup

To get started locally:

```bash
# Clone the project
git clone https://github.com/yourusername/yt-summarizer-ia.git
cd yt-summarizer-ia

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd tests/test_frontend
npm install
cd ../..

# Run the app locally
bash run.sh
```

---

## 🧪 Run the Tests

### Python (backend)

```bash
pytest
```

### JavaScript (frontend)

```bash
cd tests/test_frontend
npm test
```

---

## 🧠 Guidelines

- Follow PEP8 and clean coding practices
- Write docstrings and comments for clarity
- Keep PRs focused and small if possible
- Add tests if your code introduces new behavior
- Make sure existing tests pass before pushing

---

## 🗂️ Branch Strategy

- `main`: stable, production-ready code
- `dev`: latest development version
- Create feature branches from `dev` (ex: `feature/add-dark-mode`)

---

## 📝 How to Contribute

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your message"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request on the `dev` branch

---

## 📫 Questions?

Feel free to open an [Issue](https://github.com/yourusername/yt-summarizer-ia/issues) for help or to suggest improvements.

Let’s build something great together 💡