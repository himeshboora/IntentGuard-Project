from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
import warnings

warnings.filterwarnings("ignore")

app = FastAPI(title="IntentGuard API")

# This is critical: It allows your Chrome Extension to talk to this local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading IntentGuard AI Model for API...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define what data the Chrome Extension will send us
class ScanRequest(BaseModel):
    commit_message: str
    code_snippet: str

@app.post("/scan")
def scan_commit(request: ScanRequest):
    # 1. AST Check (Simplified for the API MVP)
    ast_action = "Standard code updates"
    if "system(" in request.code_snippet or "socket(" in request.code_snippet:
        ast_action = "Executing OS commands and system calls"

    # 2. The AI Math
    intent_vec = model.encode(request.commit_message, convert_to_tensor=True)
    action_vec = model.encode(ast_action, convert_to_tensor=True)
    
    similarity = util.cos_sim(intent_vec, action_vec).item()
    divergence = 1.0 - max(0, similarity)

    # 3. The Verdict sent back to the browser
    return {
        "commit_message": request.commit_message,
        "divergence_score": round(divergence, 2),
        "is_malicious": divergence >= 0.5
    }