# ✈️ Airline Chatbot System using ADK & Multi-Agent Architecture

An intelligent airline customer service platform built using **Python** and the **Agent Development Kit (ADK)**. The system leverages a **multi-agent architecture**, **Retrieval-Augmented Generation (RAG)**, and **semantic search** to provide personalized passenger assistance.

## 🚀 Features

### 🤖 Multi-Agent Architecture

The chatbot is designed around specialized agents coordinated by a central **Supervisor Agent**.

| Agent                 | Responsibility                                        |
| --------------------- | ----------------------------------------------------- |
| Supervisor Agent      | Intent detection and request routing                  |
| Seat Selection Agent  | Manage seat preferences and assignments               |
| Meal Preference Agent | Handle special meal requests and dietary restrictions |
| Travel Document Agent | RAG-based travel regulations and visa assistance      |

---

## 🧠 Intelligent Intent Routing

The Supervisor Agent analyzes natural language queries and dynamically routes requests to the appropriate specialized agent.

Example:

```
User: I need a window seat for booking XYZ789

→ Supervisor Agent
    → Seat Selection Agent
        → Mock Booking API
```

This modular design allows new agents to be integrated with minimal changes.

---

## 📚 RAG-Powered Travel Assistant

The Travel Document Agent implements a Retrieval-Augmented Generation pipeline.

### Pipeline

1. PDF document ingestion
2. Text extraction
3. Intelligent chunking
4. Embedding generation
5. Vector similarity search
6. Context retrieval
7. LLM response generation with citations

### Knowledge Base

* Visa Requirements
* Passport Validity Rules
* COVID-19 Travel Regulations
* Entry Restrictions

---

## 🔄 Context-Aware Conversations

The chatbot maintains session context across interactions.

Example:

```
User: I need a halal meal.
Bot: Which booking are you referring to?
User: XYZ789
Bot: Halal meal confirmed for Jane Smith.
```

The system preserves customer and booking information throughout the conversation.

---

## 🔌 Mock Airline Backend APIs

The project includes simulated airline backend services:

* Get Booking Details
* Update Seat Assignment
* Update Meal Preference
* Aircraft Seat Layout
* Meal Catalog
* Flight Connection Information

These APIs mimic real-world airline operations without requiring external integrations.

---

## 📁 Project Structure

```
AIRLINE_CHATBOT
│
├── app
│   ├── Meal_Preference_Agent
│   ├── Seat_Selection_Agent
│   ├── Supervisor_Agent
│   └── Travel_Agent
│
├── Data
│   └── SPAIN-VISA-REQUIREMENTS.pdf
│
├── API_Server.py
├── Mock_DB.sql
├── requirements.txt
└── travel_kb_builder.py
```

---

## 💡 Architectural Highlights

* Modular ADK-based multi-agent system
* Supervisor-driven orchestration
* Retrieval-Augmented Generation (RAG)
* Semantic vector search
* Context-aware session management
* Extensible agent design
* Mock backend service simulation
* Clean separation between business logic and knowledge retrieval

---

## 🛠️ Technology Stack

* Python
* Agent Development Kit (ADK)
* SQLite
* Vector Database
* PDF Processing
* Embeddings & Semantic Search
* REST-style Mock APIs

---

## ▶️ Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the API Server

```bash
python API_Server.py
```

### Build the Travel Knowledge Base

```bash
python travel_kb_builder.py
```

---

## 💬 Sample Queries

### Seat Selection

```
I want to change my seat to a window seat for booking XYZ789
```

### Meal Preference

```
I need a halal meal for my flight
```

### Travel Documents

```
Do I need a visa to travel from Singapore to Malaysia?
```

---

## 🔮 Future Enhancements

* Flight Booking Agent
* Baggage Management Agent
* Check-in Agent
* Loyalty Program Agent
* Live Airline API Integration
* Multi-language Support
* Voice-based Interaction
* Agent Memory for Personalized Recommendations

---

## 📌 Project Objective

This project demonstrates how **Generative AI, Multi-Agent Systems, and RAG architectures** can be combined to build scalable, intelligent customer service solutions for the airline industry.
