from fastapi import FastAPI # Import FastAPI framework
from fastapi.middleware.cors import CORSMiddleware # Importing CORS middleware
from pydantic import BaseModel
from transformers import pipeline
from backend.app.claim_filter import extract_claims
from backend.app.verifier import verify_claim
from backend.app.image_detection.detector import ImageDetector


print("Loading AI detector...")

ai_detector = pipeline(
    "text-classification",
    model="ogmatrixllm/glyph-v1.1"
)

print("AI detector loaded!")

# We load the model before request, because loading model for every request will be painfully slow

class PageData(BaseModel):
    title: str
    text: str

class TextDetectionRequest(BaseModel):
    text: str

class ClaimExtractionRequest(BaseModel):
    text: str

class VerifyClaimRequest(BaseModel):
    claim: str

class ImageRequest(BaseModel):
    image_path: str

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

@app.post("/analyze")# When someone visits '/analyze', run the below function
# Third endpoint
def analyze_page(data: PageData):

    word_count = len(data.text.split())

    character_count = len(data.text)

    return {
        "title": data.title,
        "word_count": word_count,
        "character_count": character_count,
        "analysis": "Processed by FastAPI"
    }

@app.post("/detect_text_ai")
def detect_text_ai(data: TextDetectionRequest):

    result = ai_detector(data.text)[0]

    label = result["label"]
    score = result["score"]

    if label == "LABEL_1":
        classification = "AI Generated"
        ai_probability = score * 100
    else:
        classification = "Human Written"
        ai_probability = (1 - score) * 100

    return {
        "classification": classification,
        "ai_probability": round(ai_probability, 2)
    }

@app.post("/extract_claims")
def extract_claims_endpoint(
    data: ClaimExtractionRequest
):

    claims = extract_claims(data.text)

    return {
        "claims": claims,
        "claim_count": len(claims)
    }

@app.post("/verify_claim")
def verify_claim_endpoint(
    data: VerifyClaimRequest
):

    result = verify_claim(data.claim)

    return {
        "claim": data.claim,
        "status": result["status"],
        "confidence": result["confidence"]
    }

image_detector = ImageDetector()

@app.post("/detect_ai_image")
def detect_ai_image(request: ImageRequest):

    result = image_detector.predict(
        request.image_path
    )

    return result