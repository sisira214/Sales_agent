
# Sales Agent 🚀

A simple AI-powered **Sales Agent** application built with **FastAPI**, **LangChain**, and a **Streamlit** UI for interactive customer engagement. This project exposes a backend API for the agent and a frontend interface to interact with it. 

---

## 🧠 Overview

The **Sales Agent** is designed to automate basic sales conversations, product recommendations, and customer engagement using large language models. The backend runs as a FastAPI service, and the frontend uses Streamlit to stream chat interactions with the agent. :contentReference[oaicite:1]{index=1}

---

## 🚀 Features

- 🛠️ FastAPI backend serving the sales agent API  
- 🤖 LangChain integration for AI-driven responses and workflow  
- 📊 Streamlit UI for real-time chat interactions  
- 🧩 Simple and extensible architecture for adding more sales logic  
- ⚡ Easily deployable and testable locally :contentReference[oaicite:2]{index=2}

---

## 🧰 Tech Stack

| Feature            | Technology      |
|--------------------|-----------------|
| Backend API        | FastAPI         |
| Sales Logic        | LangChain       |
| Frontend UI        | Streamlit       |
| Language           | Python          |
| Deployment         | Local / Cloud   | :contentReference[oaicite:3]{index=3}

---

## 📦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sisira214/Sales_agent.git
cd Sales_agent
````

### 2. Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file (if needed) and add your API keys or settings such as:

```env
OPENAI_API_KEY="your_api_key_here"
# Add any other keys your agent requires
```


---

## 🧪 Run Backend API

```bash
uvicorn agentAPI:app --reload
```

This starts your FastAPI server (usually at `http://localhost:8000`).
You can test endpoints like `/docs` for interactive API docs.

---

## ✨ Run Streamlit UI

```bash
streamlit run sales_streamlit.py
```

This opens a browser interface where you can interact with the sales agent in real time.

---

## 🧠 How It Works

1. The **Streamlit UI** sends user messages to the backend API.
2. The **FastAPI server** passes the text to LangChain logic (in `Sales_langchain.py`).
3. LangChain formats the prompt, calls the model, and returns responses.
4. Responses are streamed back to the UI for real-time chat experience.

*(Edit this as needed to more accurately reflect your app’s message flow.)*

---

## 📁 Project Structure

```
Sales_agent/
├── .gitignore
├── LICENSE
├── README.md
├── Sales_langchain.py    # Sales logic using LangChain
├── agentAPI.py          # FastAPI backend
├── sales_streamlit.py   # Streamlit UI
└── requirements.txt     # Dependencies
```

---

## 🤝 Contributing

Contributions are welcome! You can help by:

* Improving conversation logic
* Adding support for more sales workflows
* Enhancing UI/UX
* Writing tests or examples

Please open issues or pull requests on GitHub.

---

## 📜 License

This project is licensed under the **MIT License** — see the `LICENSE` file for details. 



[1]: https://github.com/sisira214/Sales_agent "GitHub - sisira214/Sales_agent: Implemented fast API and stream the sales agent through it"
