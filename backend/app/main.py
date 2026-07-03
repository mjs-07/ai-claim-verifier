from fastapi import FastAPI # Import FastAPI framework
from fastapi.middleware.cors import CORSMiddleware # Importing CORS middleware
from pydantic import BaseModel
from transformers import pipeline
from backend.app.claim_filter import extract_claims
from backend.app.verifier import verify_claim
# from backend.app.image_detection.detector import ImageDetector
from backend.app.claim_normalizer import normalize_claims


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

class AnalyzeRequest(BaseModel):
    text: str

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

@app.post("/page_analysis")# When someone visits '/page_analysis', run the below function
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
def run_ai_detection(data: TextDetectionRequest):

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
    normalized_claims = normalize_claims(claims)

    # ----------------------------------
    # Fallback:
    # If no factual claims are extracted,
    # verify the selected text itself.
    # ----------------------------------

    if len(normalized_claims) == 0:
        selected_text = data.text.strip()
        if selected_text:
            normalized_claims = [selected_text]
            
    return {
        "claims": normalized_claims,
        "claim_count": len(normalized_claims)
    }

@app.post("/verify_claim")
def verify_claim_endpoint(
    data: VerifyClaimRequest
):

    return verify_claim(data.claim)

@app.post("/analyze")
def analyze_text(data: AnalyzeRequest):

    # -----------------------------
    # AI Detection
    # -----------------------------

    ai_result = run_ai_detection(
        TextDetectionRequest(
            text=data.text
        )
    )

    # -----------------------------
    # Claim Extraction
    # -----------------------------

    claims_result = extract_claims_endpoint(
        ClaimExtractionRequest(
            text=data.text
        )
    )

    verification_results = []

    # -----------------------------
    # Verify Every Claim
    # -----------------------------

    for claim in claims_result["claims"]:

        result = verify_claim(claim)

        verification_results.append(result)

    # -----------------------------
    # Overall Statistics
    # -----------------------------

    supported = sum(
        1
        for r in verification_results
        if r["status"] == "Supported"
    )

    contradicted = sum(
        1
        for r in verification_results
        if r["status"] == "Contradicted"
    )

    unknown = sum(
        1
        for r in verification_results
        if r["status"] not in (
            "Supported",
            "Contradicted"
        )
    )

    # -----------------------------
    # Overall Credibility
    # -----------------------------

    overall_credibility = None

    if verification_results:

        overall_credibility = round(

            sum(
                r["credibility"]["credibility_score"]
                for r in verification_results
            )

            /

            len(verification_results),

            2

        )

    # -----------------------------
    # Response
    # -----------------------------

    return {

        "ai_detection": ai_result,

        "claims_found":

            len(claims_result["claims"]),

        "supported_claims":

            supported,

        "contradicted_claims":

            contradicted,

        "unknown_claims":

            unknown,

        "overall_credibility":

            overall_credibility,

        "verification_results":

            verification_results

    }

# image_detector = ImageDetector()

# @app.post("/detect_ai_image")
# def detect_ai_image(request: ImageRequest):

#     result = image_detector.predict(
#         request.image_path
#     )

#     return result