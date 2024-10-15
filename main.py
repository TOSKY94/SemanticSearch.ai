
from fastapi import FastAPI
from app.api.endpoints import router as api_router

# Initialize FastAPI app
app = FastAPI(
    title="Semantic Search API",
    description="An API for storing and retrieving text chunks using semantic search.",
    version="1.0.0"
)

# Include the API router from the app/api/endpoints.py file
app.include_router(api_router)

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Semantic Search API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







