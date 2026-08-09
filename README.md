# 🤖 SmartOfficeAI

**SmartOfficeAI** is an Agentic AI-powered office assistant built with Python, LangChain, LangGraph, Gemini, RAG, memory, and Streamlit.

It combines conversational AI with office automation capabilities such as document question answering, email automation, calendar event creation, intelligent intent detection, and persistent memory.

## 🚀 Features

* 🤖 Agentic AI conversational assistant
* 📚 Retrieval-Augmented Generation (RAG)
* 🧠 Short-term and long-term memory
* 🔗 LangChain and LangGraph workflow
* 📧 Email automation
* 📅 Calendar event creation
* 🎯 Smart intent detection
* 🔍 Semantic document search
* 🗄️ SQLite database
* 📦 ChromaDB vector database
* 🎨 Streamlit web interface

## 🏗️ Project Architecture

```text
SmartOfficeAI/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── Database components
│
├── graph/
│   └── LangGraph workflow
│
├── memory/
│   └── AI memory management
│
├── prompts/
│   └── Prompt templates
│
├── rag/
│   └── RAG and document retrieval
│
├── tools/
│   └── Email and calendar tools
│
└── uploaded_docs/
    └── Documents for RAG
```

## 🛠️ Technologies

* Python
* LangChain
* LangGraph
* Google Gemini
* RAG
* ChromaDB
* Sentence Transformers
* SQLite
* Streamlit

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/mohammednasim/SmartOfficeAI.git
cd SmartOfficeAI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-2.5-flash
```

**Never commit your `.env` file or API keys to GitHub.**

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🎯 Main Use Cases

### AI Chat Assistant

Interact with the AI assistant using natural language.

### Document Q&A

Upload documents and ask questions using RAG-based retrieval.

### Email Automation

Generate and send emails using the integrated email tool.

### Calendar Automation

Create calendar events from natural-language instructions.

### Memory

Maintain relevant conversation and application information across interactions.

## 📌 Future Improvements

* Voice-based AI assistant
* More enterprise integrations
* Advanced multi-agent workflows
* Web search integration
* Improved authentication and user management
* Cloud deployment
* Advanced analytics dashboard

## 👨‍💻 Author

**Mohammed Nasim P**

GitHub: https://github.com/mohammednasim

## 📄 License

This project is intended for educational and portfolio purposes.
