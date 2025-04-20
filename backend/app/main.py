# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, spaces, contents, generate

app = FastAPI(
    title="VideoSage API",
    description="Backend API for VideoSage application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(spaces.router, prefix="/api/spaces", tags=["spaces"])
app.include_router(contents.router, prefix="/api/contents", tags=["contents"])
app.include_router(generate.router, prefix="/api/generate", tags=["generate"])

@app.get("/")
async def root():
    return {"message": "Welcome to VideoSage API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)