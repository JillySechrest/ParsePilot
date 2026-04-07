from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import documents, chat

## Create instance
app = FastAPI(
    title="ParsePilot API",
    description="ParsePilot API for document parsing and chat interactions",
    version="1.0.0"
)

# --- CORS MIDDLEWARE ---
# CORS config to allow frontend requests
# frontend running on http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], # All CRUD methods
    allow_headers=["*"], # Allow all headers
)

# --- REGISTER ROUTES ---
# Doc route
app.include_router(documents.router, 
                   prefix="/api/documents", 
                   tags= ["Documents"])
# Chat route
app.include_router(chat.router, 
                   prefix="/api/chat",
                   tags=["Chat"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}