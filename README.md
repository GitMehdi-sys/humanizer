# Humanizer Web App 🧠✨

Humanizer is a Python-based web application that converts raw or technical content into more **human-friendly formats**.  
It supports:

- 📊 Number humanization (e.g. `1234567 → 1,234,567`)
- 💾 File size formatting
- ⏱️ Time formatting
- ✍️ AI-powered text humanization using OpenAI
- 🌐 Web interface built with FastAPI + Jinja2

This project is structured as a **real Python package + web application**, following professional software architecture.

---

## 🚀 Features

- Modern `src/` Python package layout
- FastAPI backend
- HTML frontend with Jinja2 templates
- AI text rewriting to sound natural
- Extendable and modular design
- Local development mode with hot reload

---

## 🧱 Project Structure

humanizer/
│
├── src/
│ └── humanize/ # Core logic library
│
├── webapp/
│ ├── main.py # FastAPI web server
│ ├── templates/ # HTML pages
│ └── static/ # CSS / assets
│
├── pyproject.toml
└── README.md


---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/GitMehdi-sys/humanizer.git
cd humanizer
2. Install dependencies
python -m pip install -r requirements.txt
(or if using editable mode)

python -m pip install -e .
🔑 OpenAI API Setup (for text humanization)
To enable AI text rewriting, you need an OpenAI API key.

Steps:
Create a key at:
https://platform.openai.com/api-keys

Add your key in humanize.py:

openai.api_key = "YOUR_API_KEY"
⚠️ Do not publish your API key publicly.

▶️ Run the Web App
From the project root:

uvicorn webapp.main:app --reload
🌐 Open in browser
http://127.0.0.1:8000
📖 API Documentation
FastAPI automatically provides interactive API docs:

http://127.0.0.1:8000/docs
🧪 Example Usage
Humanize a number
/number?n=1234567
Humanize text
Use the Text Humanizer page and paste your content.

🛠️ Built With
Python 3.10+

FastAPI

Jinja2

OpenAI API

Humanize library

HTML / CSS

🎯 Future Improvements
User authentication

Dark mode UI

History of humanized texts

AI model selection

Deployment to Render / Railway

👨‍💻 Author
Elmehdi Elmouate
Software Engineering Student
Python | Web Dev | AI Enthusiast

⭐ If you like this project
Give it a star on GitHub ⭐


