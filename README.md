# VectorLoom

## AI-Powered Hybrid Fashion Recommendation & Context-Aware AI Platform

VectorLoom is an intelligent recommendation platform built around the **H&M Fashion Dataset**. It combines customer behavior and product characteristics to generate personalized fashion recommendations using a **hybrid recommendation approach**.

The project also includes a context-aware RAG pipeline that can ingest documents, retrieve relevant information using semantic and keyword search, rerank the results, and generate grounded answers through an LLM.

---

## 🎯 Project Objective

The primary objective of VectorLoom is to demonstrate how an intelligent recommendation system can combine multiple sources of information instead of relying on a single recommendation strategy.

VectorLoom combines:

- **Collaborative Filtering** — learns from customer interaction patterns.
- **Content-Based Filtering** — uses product attributes and descriptions.
- **Hybrid Recommendation** — combines collaborative and content signals.
- **Top-N Ranking** — returns the highest-ranked products for a customer.

The platform also provides a RAG-based conversational layer for querying uploaded documents.

---

## 🏗️ High-Level Architecture

```text
                         VECTORLOOM
                              │
              ┌───────────────┴────────────────┐
              │                                │
       Recommendation Engine             RAG / AI Assistant
              │                                │
      ┌───────┴────────┐               ┌───────┴────────┐
      │                │               │                │
 Customer Behavior  Product Data    Documents       User Query
      │                │               │                │
      ▼                ▼               ▼                ▼
Collaborative      Content-Based   Ingestion        Query Rewrite
Filtering          Filtering       & Chunking            │
      │                │               ▼                  ▼
      └───────┬────────┘          Embeddings        Vector Search
              ▼                         │                  │
       Hybrid Scoring                   ├────────┐         │
              │                         │        │         │
              ▼                      ChromaDB  BM25       │
          Ranking                       │        │         │
              │                         └───┬────┘         │
              ▼                             ▼              │
        Top-N Products                  Hybrid Retrieval
              │                             │
              ▼                             ▼
         FastAPI API                    Reranking
              │                             │
              ▼                             ▼
          Frontend                         LLM
                                            │
                                            ▼
                                        Citations
```

---

## 📊 Dataset

VectorLoom uses the H&M fashion dataset.

The product catalogue contains **105,542 articles** and 25 product-related attributes.

Important product attributes include:

| Attribute | Description |
|---|---|
| `article_id` | Unique product identifier |
| `product_code` | Product code |
| `prod_name` | Product name |
| `product_type_name` | Product type |
| `product_group_name` | Product group |
| `colour_group_name` | Product colour |
| `department_name` | Department |
| `section_name` | Store section |
| `garment_group_name` | Garment group |
| `detail_desc` | Product description |

Example product:

```text
Product: Hood W Zip
Type: Hoodie
Colour: Dark Green
Group: Garment Upper body
Description:
Long-sleeved jacket in sweatshirt fabric with a lined drawstring hood,
zip down the front, side pockets and ribbing at the cuffs and hem.
```

---

# 🧠 Recommendation Engine

## Why Hybrid Recommendation?

A recommendation system can use different signals to determine what a customer may like.

### Collaborative Filtering

Collaborative filtering answers:

> "What products are preferred by customers with similar behavior?"

It uses customer interaction patterns to identify relationships between customers and products.

### Content-Based Filtering

Content-based filtering answers:

> "What products are similar to products that are relevant to this customer?"

It uses product characteristics such as:

- product type
- product group
- colour
- department
- section
- description

### Hybrid Recommendation

VectorLoom combines both approaches:

```text
Customer Behavior
        │
        ▼
Collaborative Score
        │
        ├──────────────┐
        │              │
        │          Hybrid Model
        │              │
Product Features      │
        │              │
        ▼              │
Content Score ────────►│
                       ▼
                  Hybrid Score
                       │
                       ▼
                     Rank
                       │
                       ▼
                  Top-N Items
```

This allows VectorLoom to consider both **customer behavior** and **product similarity**.

---

# 🔎 Example Recommendation

For a demonstration customer:

```text
Customer ID:
75c54a755b8a467e53e0a4e01833deb029734feb22ad25438137925123a38f8b
```

VectorLoom successfully returned personalized recommendations.

Example:

| Product | Collaborative | Content | Hybrid | Reason |
|---|---:|---:|---:|---|
| Hood W Zip — Dark Green | 0.8656 | 5.1693 | 0.3234 | Collaborative + Content |
| Hood W Zip — Black | 0.0680 | 5.4680 | 0.3031 | Collaborative + Content |
| Hood W Zip — Dark Grey | 0.0630 | 5.3302 | 0.2953 | Collaborative + Content |
| Hood W Zip — White | 0.0000 | 5.3482 | 0.2934 | Content |
| Hood W Zip — Grey | 0.0000 | 5.3045 | 0.2910 | Content |

The final recommendation score is used to rank products and return the highest-scoring items.

---

# 🤖 RAG / Context-Aware AI Assistant

VectorLoom also implements a document-based RAG pipeline.

Current pipeline:

```text
User Question
      │
      ▼
Query Rewriting
      │
      ▼
Cache Lookup
      │
      ▼
Vector Retrieval
      │
      ▼
Hybrid Retrieval
   ┌──┴──┐
   ▼     ▼
Vector  BM25
Search  Search
   │     │
   └──┬──┘
      ▼
Result Merging
      │
      ▼
Cross-Encoder Reranking
      │
      ▼
Prompt Construction
      │
      ▼
LLM Generation
      │
      ▼
Citation Generation
      │
      ▼
Conversation Memory
      │
      ▼
Grounded Response
```

The system currently supports documents such as:

- Salesforce Administration notes
- Apex and Trigger notes
- text documents

Example question:

> What is a Salesforce trigger?

VectorLoom retrieves relevant document chunks and generates an answer using the retrieved context.

---

# 🔀 Hybrid Retrieval

VectorLoom does not rely exclusively on vector similarity.

It combines:

### Semantic / Vector Search

Useful for understanding the meaning of a question.

### BM25

Useful for exact keywords and lexical matches.

### Result Merging

The two result sets are combined before reranking.

### Cross-Encoder Reranking

The candidate documents are then evaluated for relevance to the actual query.

This produces a stronger retrieval pipeline than using only one retrieval strategy.

---

# ⚙️ Backend API

VectorLoom exposes its functionality through FastAPI.

### Health

```http
GET /api/v1/health
```

Example:

```json
{
  "status": "healthy"
}
```

### Documents

```http
GET /api/v1/documents/
POST /api/v1/documents/upload
GET /api/v1/documents/{document_name}
```

### RAG Chat

```http
POST /api/v1/chat/chat
POST /api/v1/chat/chat-stream
```

### Recommendations

```http
GET /api/v1/recommendations/{customer_id}
```

Example:

```http
GET /api/v1/recommendations/{customer_id}?limit=5
```

---

# 🧰 Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## Recommendation System

- pandas
- H&M Dataset
- Collaborative Filtering
- Content-Based Filtering
- Hybrid Ranking

## RAG

- ChromaDB
- Vector Embeddings
- BM25
- Cross-Encoder Reranking
- Ollama
- Llama 3.2

## Frontend

- Streamlit

## Development

- Git
- GitHub
- Python Virtual Environment

---

# 📁 Project Structure

```text
VectorLoom/
│
├── data/
│   ├── hm/
│   ├── models/
│   └── ...
│
├── frontend/
│   └── app.py
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── chat.py
│   │       ├── chat_stream.py
│   │       ├── documents.py
│   │       └── recommendations.py
│   │
│   ├── cache/
│   ├── citation/
│   ├── core/
│   ├── embeddings/
│   ├── ingestion/
│   ├── llm/
│   ├── memory/
│   ├── models/
│   ├── query_rewriter/
│   ├── recommendation/
│   ├── reranker/
│   ├── retrieval/
│   └── schemas/
│
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

# 🚀 Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/MohammedTouqeerUrRaiyan/VectorLoom.git
cd VectorLoom
```

## 2. Create virtual environment

```powershell
python -m venv venv
```

## 3. Activate environment

```powershell
.\venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## 5. Start FastAPI

```powershell
python -m uvicorn src.api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 6. Start Streamlit

In another terminal:

```powershell
streamlit run frontend/app.py
```

Frontend:

```text
http://localhost:8501
```

---

# 🧪 Current API Validation

The current implementation has been tested successfully for:

### Health

```text
GET /api/v1/health
→ {"status":"healthy"}
```

### Document Listing

```text
GET /api/v1/documents/
```

Currently returns indexed documents and chunk counts.

### Recommendation API

The recommendation endpoint successfully supports:

```text
Default recommendation count
Custom limit
Invalid customer handling
Product metadata
Collaborative score
Content score
Hybrid score
Recommendation reason
```

### RAG Chat

The chat endpoint successfully processes questions such as:

```text
"What is a Salesforce trigger?"
```

and returns an LLM-generated answer grounded in retrieved document context.

---

# 📈 Evaluation

The recommendation system was evaluated using Top-K recommendation metrics.

| Metric | @5 | @10 | @20 |
|---|---:|---:|---:|
| Precision | 0.0228 | 0.0130 | 0.0077 |
| Recall | 0.1140 | 0.1300 | 0.1550 |
| Hit Rate | 0.1140 | — | — |

These results provide a baseline for evaluating and improving the recommendation pipeline.

---

# 💡 Key Engineering Decisions

### Why FastAPI?

FastAPI provides:

- high-performance API serving
- automatic OpenAPI documentation
- Pydantic validation
- clean route organization
- easy integration with Python ML components

### Why Hybrid Recommendation?

Collaborative filtering captures behavior while content-based filtering captures product characteristics. Combining them gives the system multiple signals for ranking.

### Why BM25 + Vector Search?

Vector search captures semantic similarity while BM25 handles exact lexical matches. Combining both improves retrieval robustness.

### Why Reranking?

Initial retrieval creates candidate documents. A cross-encoder can then perform a more focused relevance assessment before the context is sent to the LLM.

### Why Streaming?

Streaming allows the system to return generated content progressively rather than waiting for the complete LLM response.

---

# 🔮 Future Scope

Potential improvements include:

- Customer login and authentication
- Personalized customer dashboard
- H&M-style recommendation interface
- Product image integration
- Cold-start recommendation strategy
- Online recommendation updates
- Improved recommendation evaluation
- Recommendation explanations
- Cloud deployment
- Production database integration
- Monitoring and observability
- Scalable model serving

---

# 🎯 Project Outcome

VectorLoom demonstrates an end-to-end intelligent AI platform combining:

```text
Data
 ↓
Recommendation Models
 ↓
Hybrid Ranking
 ↓
FastAPI
 ↓
Retrieval
 ↓
Reranking
 ↓
LLM
 ↓
Context-Aware Responses
```

The project focuses on demonstrating how recommendation systems and retrieval-augmented AI components can be integrated into a practical application architecture.

---

## 👨‍💻 Project

**VectorLoom**

**Repository:**  
https://github.com/MohammedTouqeerUrRaiyan/VectorLoom

**Author:**  
Mohammed Touqeer Ur Raiyan

---

> **Note:** The current project is an internship/MVP implementation. Some capabilities listed under Future Scope are intentionally separated from the currently implemented system and should not be presented as production features.
