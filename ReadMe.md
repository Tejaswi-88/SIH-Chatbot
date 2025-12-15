 sih-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI entry point
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat_routes.py             # Chat endpoint (handles user queries)
│   │   │   ├── admin_routes.py            # File upload (PDF/Excel) & dashboard APIs
│   │   │   └── health_routes.py           # Health check endpoint
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── message_model.py           # Chat messages schema
│   │   │   ├── user_model.py              # User schema
│   │   │   └── document_model.py          # Knowledge base doc schema (PDF/Excel)
│   │   ├── db/
│   │   │   ├── connection.py              # MongoDB connection logic (Motor)
│   │   │   └── queries.py                 # CRUD and aggregation operations
│   │   ├── services/
│   │   │   ├── language_service.py        # Language detection + transliteration
│   │   │   ├── translation_service.py     # Translation between languages
│   │   │   ├── nlp_service.py             # Intent detection, entity recognition
│   │   │   ├── rag_service.py             # Embedding, FAISS search, retrieval
│   │   │   ├── pdf_parser.py              # Extract text from PDFs
│   │   │   ├── excel_parser.py            # Read and structure data from Excel
│   │   │   └── tts_service.py             # Optional: text-to-speech output
│   │   ├── utils/
│   │   │   ├── helpers.py                 # Utility helpers (formatting, cleaning)
│   │   │   ├── logger.py                  # Logging setup
│   │   │   └── config_loader.py           # Read .env / config variables
│   │   ├── config.py                      # Centralized settings/configuration
│   │   └── __init__.py
│   │
│   ├── data/                              # Sample data / test docs / embeddings
│   │   ├── faiss_index/
│   │   ├── uploads/
│   │   └── samples/
│   ├── venv/
│   ├── .gitignore
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx             # Chat UI component
│   │   │   ├── MessageBubble.jsx          # Display each message
│   │   │   ├── LanguageSelector.jsx       # Dropdown for language preference
│   │   │   └── FileUpload.jsx             # Admin upload component (PDF/Excel)
│   │   ├── pages/
│   │   │   ├── Chat.jsx                   # Main chatbot page
│   │   │   └── AdminDashboard.jsx         # File upload + logs dashboard
│   │   ├── App.js
│   │   ├── api.js                         # Handles Axios API calls to backend
│   │   └── i18n/                          # Frontend multilingual setup (optional)
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── README.md
│
├── logs/
│   ├── backend.log
│   ├── frontend.log
│   └── access.log
│
├── scripts/
│   ├── ingest_docs.py                     # Standalone script to populate FAISS DB
│   ├── test_api.py                        # Local script to test backend endpoints
│   └── init_setup.sh                      # Optional automation script for setup
│
├── docs/
│   ├── architecture_diagram.png
│   ├── api_endpoints.md
│   ├── workflow_explanation.md
│   └── setup_guide.md
│
├── .dockerignore
├── .env
├── docker-compose.yml
└── README.md





 
 
 
 /sih-chatbot
│
├── /frontend                   # React app for the chat UI
│   ├── /public                 # Public files (index.html, images, etc.)
│   ├── /src                    # Source files for React components
│   ├── Dockerfile              # Dockerfile for React app
│   ├── package.json            # Dependencies for React app
│   └── .env                    # Environment variables (if needed)
│
├── /backend                    # FastAPI backend
│   ├── /app                    # FastAPI source code (API logic)
│   ├── /models                 # Backend models (user, KB, etc.)
│   ├── /data                   # Directory for storing documents/PDFs, etc.
│   ├── Dockerfile              # Dockerfile for FastAPI backend
│   ├── requirements.txt        # Python dependencies (FastAPI, etc.)
│   ├── .env                    # Environment variables (MongoDB URI, etc.)
│   └── main.py                 # Entry point for FastAPI
│
├── /docker-compose.yml         # Docker Compose file to link frontend and backend
├── /docs                       # Documentation (README, API docs, etc.)
├── /logs                       # Logs directory (for development/testing)
└── /scripts                    # Utility scripts (data ingestion, etc.)

sih-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── __pycache__/
│   ├── data/
│   ├── modules/
│   ├── venv/
│   ├── .gitignore
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── node_modules/
│   ├── Dockerfile
│   ├── package.json
│   └── package-lock.json
│
├── logs/
├── scripts/
├── docs/
├── .dockerignore
├── .env
└── docker-compose.yml



app/
 ├── main.py
 ├── routes/
 │    ├── __init__.py
 │    └── chat_routes.py
 ├── models/
 │    ├── __init__.py
 │    └── message_model.py
 ├── db/
 │    └── connection.py
 ├── utils/
 │    └── helpers.py
 ├── config.py
 └── __init__.py



frontend/
 ├── src/
 │    ├── components/
 │    ├── pages/
 │    │    └── Chat.jsx
 │    ├── App.js
 │    └── api.js
 ├── package.json
 └── Dockerfile



mkdir sih-chatbot
cd sih-chatbot
mkdir frontend backend docs scripts logs

cd frontend
npx create-react-app .
npm install tailwindcss # Install tailwind if you want to use it

Create backend folder structure (FastAPI app):
cd backend
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows

Install FastAPI and other dependencies:
pip install fastapi uvicorn pymongo sentence-transformers faiss-cpu openpyxl python-dotenv
pip freeze > requirements.txt
pip list


Create the folder structure:
mkdir app models data
touch app/main.py requirements.txt


WSL
------------------------------------------
new terminal
v - dropdown
select ubuntu

Docker
-----------------------------------------------
Step 1:Build the containers
docker compose build
This will build both frontend and backend images based on the Dockerfiles we created.
First time may take a few minutes because it installs dependencies and builds the React app.

Step 2: Start the containers
docker compose up
This starts both frontend (Nginx) and backend (FastAPI) containers.
You’ll see logs from both services in your terminal.
Notes:
Press CTRL+C to stop the containers in this terminal.
To run in detached mode (background), use:
docker compose up -d


docker compose up -d  ------ container runes even if the terminal is closed 
docker compose down ------- to stop container

✅ Summary:

Action	Command
Build new images (if Dockerfile or dependencies change) ---	docker compose build
Start containers ---	docker compose up -d
View running containers ---	docker ps
View logs ---	docker compose logs -f
Stop containers	 --- docker compose down