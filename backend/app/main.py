from fastapi import FastAPI # Import FastAPI framework
from fastapi.middleware.cors import CORSMiddleware # Importing CORS middleware

app = FastAPI() # Restaurant Created

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # When someone visits '/', run the below function. 
# This is the first endpoint
def root():
    return {"message": "AI claim verifier backend is running!"}

@app.get("/health") # When someone visits '/health', run the below function
# This is the second endpoint
def health():
    return {"status": "Working"}

