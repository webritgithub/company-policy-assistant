# Employee Handbook Assistant

An AI-powered application that answers employee policy questions using information retrieved from an employee handbook. The application uses Retrieval-Augmented Generation (RAG) to provide relevant answers grounded in the handbook, along with source references.

## Live Demo

**Application:** https://company-policy-assistant-wv9f.onrender.com

**GitHub Repository:** https://github.com/webritgithub/company-policy-assistant

## Features

- **Natural Language Questions:** Ask questions about employee policies in plain English.
- **Retrieval-Augmented Generation (RAG):** Retrieves relevant handbook sections before generating an answer.
- **Semantic Search:** Uses Google Gemini embeddings and ChromaDB to find relevant information.
- **Source References:** Displays relevant handbook sections and page references alongside answers.
- **Grounded Responses:** Uses the handbook as the source of information and returns a standard message when the requested information cannot be found.
- **Web Interface:** Simple interface built with HTML, CSS, and JavaScript.
- **Cloud Deployment:** Deployed as a web application using Render.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| LLM | Google Gemini (`gemini-3.6-flash`) |
| Embeddings | Google Gemini Embeddings |
| Vector Database | ChromaDB |
| RAG Framework | LangChain |
| Document Processing | PyPDF |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |
| Production Server | Gunicorn |

## How It Works

1. **Document Loading:** The employee handbook PDF is loaded and its text is extracted.
2. **Text Chunking:** The extracted text is divided into smaller, meaningful chunks.
3. **Embedding Generation:** Gemini embeddings convert the text chunks into vector representations.
4. **Vector Storage:** The embeddings and associated text are stored in ChromaDB.
5. **Retrieval:** When a user asks a question, the system retrieves relevant handbook sections using semantic similarity.
6. **Answer Generation:** The retrieved context is passed to the Gemini language model to generate an answer.
7. **Source Display:** The application displays the answer and relevant source references in the web interface.

## Project Structure

```text
company-policy-assistant/
├── app.py
├── data/
│   └── multi_company_employee_handbook.pdf
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── retriever.py
│   ├── rag_chain.py
│   └── schemas.py
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- A Google Gemini API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/webritgithub/company-policy-assistant.git
cd company-policy-assistant
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API Key

Set the Gemini API key as an environment variable using the variable name expected by the application. For example, if the code uses `GOOGLE_API_KEY`:

**Windows PowerShell:**

```powershell
$env:GOOGLE_API_KEY="your-gemini-api-key"
```

**macOS/Linux:**

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

Replace the example value with your own API key. Never commit API keys or other secrets to GitHub.

### 5. Run the Application

```bash
python app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

The application may generate the vector database from the handbook when it starts if a usable persisted database is not available.

## Deployment

The application is deployed on Render.

Typical deployment configuration:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment Variables:** Configure the required Gemini API key in the Render dashboard.

The first request after startup may take longer if the vector database needs to be created or the hosting service has been idle.

## Example Questions

You can ask questions such as:

- What are the working hours?
- How many annual leave days are provided?
- What is the probation period?
- What is the remote work policy?
- How many sick leave days are available at a specific company?


If the requested information is not available in the handbook, the assistant responds:

> I could not find this information in the employee handbook.



---

Developed by **Ritika Poojary**
