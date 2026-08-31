from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database.db import engine, Base
from routers import auth, documents, qa, history, audit, verify
from config import settings

# Automatically create SQL tables if not existing
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered policy decision auditor with a blockchain-anchored audit trail.",
    version="1.0.0"
)

# CORS Middleware Setup
# NOTE: This explicit list allows credentialed requests from local React/Vite dev servers.
# It should be updated to include your frontend's real domain once deployed to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API Route Modules
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(qa.router)
app.include_router(history.router)
app.include_router(audit.router)
app.include_router(verify.router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)