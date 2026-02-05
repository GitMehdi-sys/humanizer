# Humanizer Web App 🧠✨

Humanizer is a Python-based web application that converts raw or technical content into more **human-friendly formats**.  
It supports:

* 📊 Number humanization (e.g. `1234567 → 1,234,567`)
* 💾 File size formatting
* ⏱️ Time formatting
* ✍️ AI-powered text humanization using OpenAI
* 🌐 Web interface built with FastAPI + Jinja2

This project is structured as a **real Python package + web application**, following professional software architecture.

---

## 🚀 Features

* Modern `src/` Python package layout
* FastAPI backend
* HTML frontend with Jinja2 templates
* AI text rewriting to sound natural
* Extendable and modular design
* Local development mode with hot reload

---

## 🧱 Project Structure

```
humanizer/
│
├── src/
│   └── humanize/          # Core logic library
│
├── webapp/
│   ├── main.py            # FastAPI web server
│   ├── templates/         # HTML pages
│   └── static/            # CSS / assets
│
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/GitMehdi-sys/humanizer.git
cd humanizer
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

(or if using editable mode)

```bash
python -m pip install -e .
```

---

## 🔑 OpenAI API Setup (for text humanization)

To enable AI text rewriting, you need an OpenAI API key.

**Steps:**

1. Create a key at:  
   https://platform.openai.com/api-keys

2. Add your key in `humanize.py`:

```python
openai.api_key = "YOUR_API_KEY"
```

⚠️ **Do not publish your API key publicly.**

---

## ▶️ Run the Web App

From the project root:

```bash
uvicorn webapp.main:app --reload
```

### 🌐 Open in browser

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically provides interactive API docs:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Usage

### Humanize a number

```
/number?n=1234567
```

### Humanize text

Use the **Text Humanizer** page and paste your content.

---

## 🛠️ Built With

* Python 3.10+
* FastAPI
* Jinja2
* OpenAI API
* Humanize library
* HTML / CSS

---

## 🎯 Future Improvements

- [ ] User authentication
- [ ] Dark mode UI
- [ ] History of humanized texts
- [ ] AI model selection
- [ ] Deployment to Render / Railway

---

## 👨‍💻 Author

**Elmehdi Elmouate**  
Software Engineering Student  
Python | Web Dev | AI Enthusiast

📧 Contact: [Your Email]  
🔗 GitHub: [@GitMehdi-sys](https://github.com/GitMehdi-sys)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:

✅ **Commercial use** - Use it in commercial projects  
✅ **Modification** - Modify and improve the code  
✅ **Distribution** - Share it with others  
✅ **Private use** - Use it privately  

**Requirements:**
- Keep the original copyright notice
- Include the license in any copies

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

---

## ⭐ If you like this project

Give it a **star** on GitHub ⭐  
Share it with friends 🚀  
Report bugs or suggest features 💡

---

## 🙏 Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
* [OpenAI](https://openai.com/) - AI text processing
* [Python Humanize](https://github.com/python-humanize/humanize) - Number formatting library
* All contributors and supporters of this project

---

**Made with ❤️ by Elmehdi Elmouate**
