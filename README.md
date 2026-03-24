# 🚀 AI-Powered Company Knowledge Base (Multimodal Semantic Search)

An AI-powered backend system that allows users to upload and search across documents and images using natural language queries.

This project implements a **multimodal semantic search engine** using vector embeddings and a vector database, enabling intelligent retrieval beyond keyword matching.

---

## ✨ Features

* 📁 Upload files (text, images)
* 🧠 Generate embeddings using:

  * Sentence Transformers (text)
  * CLIP (images)
* 🔍 Semantic search using natural language
* ⚡ Fast similarity search with ChromaDB
* 🧾 Structured API responses
* 💾 Persistent vector storage (local)

---

## 🧠 How It Works

1. User uploads a file (text/image)
2. File is processed and converted into embeddings
3. Embeddings are stored in ChromaDB
4. User enters a search query
5. Query is converted into embedding
6. Cosine similarity is used to retrieve relevant results

---

## 🏗️ Tech Stack

* **Backend:** FastAPI (Python)
* **Embeddings:**

  * `sentence-transformers`
  * `CLIP (openai/clip-vit-base-patch32)`
* **Vector Database:** ChromaDB
* **Storage:** Local filesystem
* **API Testing:** Swagger UI / Postman

---

## 📂 Project Structure

```
knowledge_base/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   ├── search.py
│   │
│   ├── services/
│   │   ├── embedder.py
│   │   ├── vector_db.py
│   │   ├── file_handler.py
│   │
│   ├── db/
│   │   ├── models.py
│   │   ├── database.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│
├── data/
├── chroma_db/
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/your-repo-name.git
cd knowledge_base
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

* Windows:

```
venv\Scripts\activate
```

* Mac/Linux:

```
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run Server

```
uvicorn app.main:app --reload
```

---

### 5️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### 📤 Upload File

```
POST /files/upload
```

Upload a text or image file.

---

### 🔍 Search

```
GET /search?query=your_query&limit=5
```

Returns semantically similar results based on query.

---

## 🧪 Example

### Query:

```
"machine learning"
```

### Result:

* Returns relevant files even if exact keywords are not present

---

## 🔥 Key Concepts Used

* Vector Embeddings
* Semantic Search
* Cosine Similarity
* Multimodal AI (Text + Image)
* Vector Databases

---

## 🚀 Future Improvements

* 📄 PDF support with chunking
* 🗄️ PostgreSQL integration for metadata
* 🔐 JWT authentication
* 🎯 Search filters (file type, date)
* 🤖 RAG (Retrieval-Augmented Generation)
* 🌐 Frontend dashboard

---

## 💼 Interview Talking Points

* Built a **multimodal semantic search system**
* Used **transformer-based embeddings** for text and images
* Integrated **vector database (ChromaDB)** for efficient retrieval
* Designed scalable backend using **FastAPI**

---

## 📜 License

MIT License

---

## 🙌 Author

Aditya Jannawar

---
