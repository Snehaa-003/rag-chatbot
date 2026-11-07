# 🔓 DecodeWher – RAG-Based DSA Chatbot

An intelligent **Retrieval-Augmented Generation (RAG) chatbot** that answers Data Structures and Algorithms (DSA) questions using a custom knowledge base.

Built using Python, LangChain, Google Gemini, FAISS, and Streamlit, the chatbot retrieves relevant information from stored documents and generates context-aware answers using an LLM.

## 🚀 Project Overview

DecodeWher is designed to help students understand DSA concepts through an interactive AI-powered chatbot.

Instead of relying entirely on the language model's general knowledge, the application retrieves relevant information from uploaded text documents and uses it as context to generate answers.

## ✨ Features

- **Document Ingestion:** Loads `.txt` documents from a local knowledge base.
- **Text Chunking:** Splits documents into smaller, overlapping chunks for better retrieval.
- **Vector Embeddings:** Converts text chunks into embeddings using Google Gemini.
- **Semantic Search:** Uses FAISS to retrieve the most relevant information.
- **AI-Powered Responses:** Generates context-aware answers using Google Gemini.
- **Source Tracking:** Displays the source documents used to generate answers.
- **Interactive UI:** Provides a chat interface using Streamlit.
- **Command-Line Interface:** Also supports interaction through a terminal.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | RAG pipeline orchestration |
| Google Gemini | Embeddings and LLM responses |
| FAISS | Vector storage and similarity search |
| Streamlit | Interactive chatbot interface |
| Python-dotenv | Environment variable management |

## 🧠 How It Works

The application follows a two-stage RAG pipeline.

### 1. Document Ingestion

1. Reads text documents from the `data/` directory.
2. Splits documents into chunks using RecursiveCharacterTextSplitter.
3. Uses a chunk size of 800 characters and an overlap of 150 characters.
4. Generates vector embeddings using Gemini.
5. Stores the embeddings in a local FAISS vector database.

### 2. Retrieval and Response Generation

1. Accepts a question from the user.
2. Converts the question into an embedding.
3. Performs similarity search against the FAISS index.
4. Retrieves the top 3 relevant chunks.
5. Passes the retrieved content and question to Gemini.
6. Generates a response grounded in the retrieved information.
7. Displays the answer along with its source documents.

## 📂 Project Structure

```text
rag-chatbot/
│
├── data/
│   ├── explanations.txt
│   └── Longest Substring Without Repeatingchar-slidingWindow.txt
│
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
│
├── app.py
├── chatbot.py
├── ingest.py
├── streamlit_app.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/Snehaa-003/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Replace the placeholder with your own Google Gemini API key.

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

To launch the Streamlit chatbot:

```bash
streamlit run streamlit_app.py
```

Alternatively, run the command-line chatbot:

```bash
python app.py
```

## 🔄 Updating the Knowledge Base

To add new DSA notes:

1. Add your `.txt` files to the `data/` directory.
2. Run the ingestion script:

```bash
python ingest.py
```

3. The FAISS index will be regenerated.
4. Restart the chatbot to use the updated knowledge base.

## 🔮 Future Improvements

- Support for PDF and DOCX document ingestion.
- Expand the knowledge base with more DSA concepts.
- Improve retrieval accuracy and response quality.
- Add conversation memory.
- Deploy the application for public access.

## 👩‍💻 Author

**Sneha**

GitHub: [@Snehaa-003](https://github.com/Snehaa-003)

---

⭐ If you find this project interesting, consider giving the repository a star!