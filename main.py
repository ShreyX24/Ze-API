# /main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import user



app = FastAPI(
    
    title="User Management API",
    description="API for managing user profiles with MongoDB backend",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",     # Development frontend
    # "https://yourapp.vercel.app" # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "User Management API is running"}