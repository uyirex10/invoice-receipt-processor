# Intelligent Invoice & Receipt Processing System

An advanced backend system that automates invoice and receipt processing using OCR, rule-based extraction, AI-assisted fallback extraction, validation pipelines, and asynchronous background processing.

---

# Features

- Upload invoices and receipts (PDF/images)
- OCR-based text extraction
- Rule-based invoice field extraction
- AI-assisted fallback extraction using Ollama
- Invoice normalization and validation
- Duplicate document detection
- Confidence scoring
- Background job queue architecture
- PostgreSQL persistence layer
- Structured logging
- Modular scalable architecture

---

# Architecture Overview

```text
Upload File
    ↓
File Storage
    ↓
Hash Generation
    ↓
Duplicate Detection
    ↓
OCR / PDF Text Extraction
    ↓
Regex-Based Extraction
    ↓
Confidence Scoring
    ↓
AI Fallback Extraction
    ↓
Normalization
    ↓
Validation
    ↓
Database Persistence
    ↓
Background Queue Processing
```

---

# Tech Stack

## Backend

- Python
- PostgreSQL
- Threading
- Queue Architecture

## OCR

- Tesseract OCR
- PDF Text Extraction

## AI

- Ollama
- Phi Local Model

## Database

- PostgreSQL
- Repository Pattern

---

# Key Engineering Concepts

This project demonstrates:

- Pipeline architecture
- Background workers
- Queue systems
- Hybrid AI architecture
- Retry logic
- Dependency injection
- Validation systems
- Data normalization
- Defensive backend engineering
- Production-oriented system design

---

# Project Structure

```text
app/
│
├── ai/
├── database/
├── extraction/
├── normalizers/
├── ocr/
├── queue/
├── services/
├── storage/
├── validators/
└── utils/

tests/
```

---

# How It Works

The system accepts uploaded invoices and receipts, extracts text using OCR or PDF parsing, then attempts deterministic regex-based field extraction.

If extraction confidence is low, the system triggers AI-assisted extraction using a local Ollama model.

Extracted data is normalized and validated before database persistence.

Processing runs asynchronously using a background worker architecture to improve scalability and responsiveness.

---

# Why Hybrid Extraction?

Regex extraction is:

- Faster
- Cheaper
- Deterministic

AI extraction is:

- More flexible
- Better for ambiguous layouts
- Slower and less predictable

This system combines both approaches to balance reliability, performance, and scalability.

---

# Scalability Considerations

Current architecture already supports:

- Background processing
- Modular services
- Queue-driven workflows
- Retry handling
- Early duplicate rejection

Future scalability improvements:

- Redis + Celery
- Distributed workers
- Cloud inference
- Batch OCR processing
- API layer with FastAPI
- Metrics and monitoring

---

# Example Use Cases

- Expense management
- Accounting automation
- AP automation
- Financial document ingestion
- Invoice processing systems
- Intelligent document processing (IDP)

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/invoice-receipt-processor.git
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create:

```text
.env
```

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/invoice_db
```

---

# Run Database Initialization

```bash
python -m app.database.init_db
```

---

# Run Full Pipeline Test

```bash
python -m tests.test_full_pipeline
```

---

# Run Background Queue Test

```bash
python -m tests.test_background_pipeline
```

---

# Important Lessons Learned

This project taught me:

- Real-world OCR is unreliable
- AI systems require guardrails
- Validation is critical
- Background workers improve scalability
- Hybrid AI systems are more practical than AI-only systems
- System architecture matters more than isolated code

---

# Future Improvements

- FastAPI API layer
- Authentication
- Expense categorization
- CSV/PDF report generation
- Accounting software integrations
- Advanced anomaly detection
- Distributed queue architecture

---

# Author

Uyi Rex

Mechanical Engineering Graduate | Backend Systems Learner | AI Automation & System Integration Enthusiast