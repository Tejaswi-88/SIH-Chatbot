from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.language_middleware import language_middleware

from app.routes.chat_routes import router as chat_router
from app.routes.health_routes import router as health_router
from app.routes.admin_routes import router as admin_router

from app.db.connection import connect_to_mongo

import uvicorn


# -----------------------------------------------------------
# ✅ FastAPI app initialization
# -----------------------------------------------------------
app = FastAPI(
    title="SIH Language-Agnostic Chatbot Backend",
    description="Multilingual chatbot with RAG, translation, and admin dashboard APIs",
    version="1.0.0"
)


# -----------------------------------------------------------
# ✅ CORS Middleware
# (React frontend will run on localhost:5173 or 3000)
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # during development → allow all # URLs that can access your API.
    allow_credentials=True,     # allows cookies/credentials if needed.
    allow_methods=["*"],        # allows all HTTP methods (GET, POST, etc.).
    allow_headers=["*"],        # allows all headers like Content-Type or Authorization
)

app.middleware("http")(language_middleware)

# -----------------------------------------------------------
# ✅ DB Startup Event
# -----------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 Connecting to MongoDB...")
    connect_to_mongo()
    print("✅ MongoDB connected.")


# -----------------------------------------------------------
# ✅ Include Routers
# -----------------------------------------------------------
app.include_router(health_router, prefix="/api/health", tags=["Health"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])


# -----------------------------------------------------------
# ✅ Root endpoint
# -----------------------------------------------------------
@app.get("/")
def root():
    return {"message": "SIH Chatbot backend is running ✅"}


# -----------------------------------------------------------
# ✅ Allow running: python main.py
# -----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
