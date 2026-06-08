from fastapi import FastAPI # Import FastAPI framework

app = FastAPI() # Restaurant Created

@app.get("/") # When someone visits '/', run the below function. 
# This is the first endpoint
def home():
    return {"message": "AI claim verifier backend is running!"}

@app.get("/ai") # When someone visits '/health', run the below function
# This is the second endpoint
def model():
    return {"status": "working"}