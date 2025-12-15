# SIH Chatbot

A full-stack AI-powered chatbot platform with document ingestion, multi-format file parsing, and a Google Gemini-powered conversational backend. Designed for rapid deployment, local development, and scalable architecture.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Project Structure](#project-structure)  
- [Setup & Installation](#setup--installation)  
- [Environment Variables](#environment-variables)  
- [Running the Project](#running-the-project)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Project Overview

SIH Chatbot is a modern, modular chatbot system capable of:

- Parsing documents in multiple formats (PDF, Word, Excel, PowerPoint)  
- Providing conversational AI responses using **Google Gemini** models  
- Storing and retrieving knowledge vectors for RAG (Retrieval-Augmented Generation) workflows  
- Supporting multilingual text-to-speech and speech-to-text via browser APIs  

The system is designed for both **local development** and **Docker-based deployment**.

---

## Features

- **Document Ingestion**: Upload PDFs, Word docs, PowerPoint presentations, and Excel sheets  
- **Knowledge Base**: Vector database storage and semantic search  
- **Conversational AI**: Gemini model integration for natural language understanding and generation  
- **Voice Support**: Text-to-speech and speech recognition  
- **Web Interface**: Frontend built with React for an intuitive chat experience  
- **Modular Backend**: Python FastAPI backend with structured services and routes  

---

## Technology Stack

**Frontend**  
- React  
- TypeScript  
- Tailwind CSS  

**Backend**  
- Python 3.11  
- FastAPI  
- SQL/Vector DB (pluggable)  
- File parsing libraries: `pdf.js`, `mammoth`, `xlsx`, `jszip`  

**AI Integration**  
- Google Gemini API (`gemini-2.5-flash`)  

**Other Tools**  
- Docker & Docker Compose  
- Git for version control  
- VS Code recommended  

---

## Project Structure

```
sih-chatbot/
├── backend/
│ ├── app/
│ │ ├── controllers/
│ │ ├── db/
│ │ ├── models/
│ │ ├── routes/
│ │ ├── services/
│ │ └── utils/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── .dockerignore
├── frontend/
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── .dockerignore
├── docs/
├── scripts/
├── logs/
├── .env
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+  
- Node.js & npm/yarn  
- Google Gemini API Key  
- Docker (optional, for containerized setup)  

### Steps

1. Clone the repository:

```bash
git clone <repo-url>
cd sih-chatbot
```
2. Create a virtual environment for Python:

```bash
python -m venv backend/venv
source backend/venv/bin/activate  # Linux/Mac
backend\venv\Scripts\activate     # Windows
```
3. Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```
4. Install frontend dependencies:

```bash
cd frontend
npm install
```
5. Copy .env.example to .env and set your API keys and configuration.

## Environment Variables

Create .env in the root folder with:
```
GEMINI_API_KEY=<your-google-gemini-api-key>
DATABASE_URL=<your-database-url>
PORT=8000
```
Other optional configs can be added depending on your backend services.

## Running the Project
### Option 1: Local Development
Backend:
```
cd backend
uvicorn app.main:app --reload
```

Frontend:
```
cd frontend
npm start
```

Visit http://localhost:3000 for the frontend interface.

## Option 2: Docker
```
docker-compose up --build
```

 - Backend will run on port 8000
 - Frontend on port 3000

### Usage
- Upload a document (PDF, Word, Excel, PowerPoint)
- Chat with the AI, ask questions about the documents
- Use voice input or output if supported in your browser

### Contributing
- Fork the repository
- Create a new feature branch
- Commit changes with descriptive messages
- Push branch and open a pull request

### License
MIT License © 2025 Tejaswi Devarapalli

