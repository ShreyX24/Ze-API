# /main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import user

app = FastAPI(
    
    title="User Management API",
    description="API for managing user profiles with MongoDB backend",
    version="1.0.0"
)

# Include routers
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "User Management API is running"}