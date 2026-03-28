# 🧠 Customer Support RAG Chatbot

A local AI-powered customer support chatbot that automatically handles
simple requests using Retrieval-Augmented Generation (RAG) and escalates
complex cases to a simulated human support workflow with ticket
creation.

------------------------------------------------------------------------

## 🚀 Overview

This project simulates a real-world **customer support automation
system** for an e-commerce company.

The chatbot:

-   🧾 Answers policy-related questions using **RAG over internal
    documents**
-   🧠 Uses a local **LLM (Qwen2.5-3B-Instruct)** to generate natural
    responses
-   🧭 Routes requests using a **rule-based triage system**
-   🎫 Escalates complex queries by creating **support tickets stored
    locally**
-   💬 Provides an interactive UI via **Streamlit**
-   🐳 Can be containerized with **Docker**

The application runs fully locally, including the LLM, which increases the container size but ensures full offline capability and zero API cost.

------------------------------------------------------------------------

## 🎯 Key Features

### 🔹 Intelligent Request Routing

-   Classifies user queries as:
    -   **Simple** → handled automatically
    -   **Complex** → escalated to human support

------------------------------------------------------------------------

### 🔹 Retrieval-Augmented Generation (RAG)

-   Uses internal policy documents (shipping, returns, refunds,
    payments)
-   Chunking with overlap
-   Embeddings via `sentence-transformers`
-   Vector search via **FAISS**

------------------------------------------------------------------------

### 🔹 Local LLM Integration

-   Model: **Qwen2.5-3B-Instruct**
-   Fully local inference (no API required)
-   Chat-style prompting with grounded context

------------------------------------------------------------------------

### 🔹 Human Handoff Simulation

-   Automatic ticket creation
-   Stored in `data/tickets.json`
-   Includes:
    -   ticket ID
    -   timestamp
    -   category
    -   reason
    -   user query

------------------------------------------------------------------------

### 🔹 Streamlit UI

-   Chat interface
-   Sidebar with routing info, retrieved chunks, and ticket details

------------------------------------------------------------------------

## 🏗️ Project Structure

    customer-support-chatbot/
    │
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── streamlit_app.py
    │
    │   ├── routing/
    │   ├── rag/
    │   ├── llm/
    │   ├── escalation/
    │   └── utils/
    │
    ├── data/
    │   ├── policies/
    │   ├── tickets.json
    │
    ├── vectorstore/
    │   ├── faiss_index.bin
    │   └── documents.pkl
    │
    ├── requirements.txt
    ├── Dockerfile
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation

``` bash
git clone https://github.com/cusiandrea/customer-support-chatbot.git
cd customer-support-chatbot
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 📦 Build Vector Store (if necessary)

``` bash
python -m app.rag.ingest
```

------------------------------------------------------------------------

## ▶️ Run the App

``` bash
python -m streamlit run app/streamlit_app.py
```

------------------------------------------------------------------------

## 🐳 Run with Docker

Pull the image:

```bash
docker pull cusiandrea/customer-support-chatbot:latest
```
Run the app:

```bash
docker run -p 8501:8501 cusiandrea/customer-support-chatbot
```

------------------------------------------------------------------------

## 🧪 Example Queries

**Simple:** - What is your return policy? - How long does shipping take?

**Complex:** - I was charged twice - My order was delivered but I didn't
receive it

------------------------------------------------------------------------

## 🧠 Tech Stack

-   Python
-   Streamlit
-   Transformers
-   FAISS
-   Sentence-Transformers
-   PyTorch

------------------------------------------------------------------------

## 📊 Architecture

    User Input
    ↓
    Rule-Based Router
    ├── Simple → RAG → LLM → Response
    └── Complex → Ticket Creation → Human Handoff

------------------------------------------------------------------------

## 📈 Future Improvements

-   ML-based routing
-   LLM fine-tuning

------------------------------------------------------------------------

## 📄 License

Educational / portfolio project.
