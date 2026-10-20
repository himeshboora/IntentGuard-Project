from sentence_transformers import SentenceTransformer, util
import warnings

warnings.filterwarnings("ignore")
print("Loading IntentGuard Core AI Model...\n")
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_divergence(commit_message, ast_action_detected):
    # 1. Convert both the human intent and the physical code action into math
    intent_vector = model.encode(commit_message, convert_to_tensor=True)
    action_vector = model.encode(ast_action_detected, convert_to_tensor=True)

    # 2. Calculate how similar they are (Cosine Similarity)
    similarity = util.cos_sim(intent_vector, action_vector).item()
    
    # 3. Calculate Divergence (1.0 minus Similarity)
    # If similarity is high, divergence is 0. If similarity is low, divergence is 1.
    divergence_score = 1.0 - max(0, similarity)

    return divergence_score

# ==========================================================
# LET'S TEST THE SYSTEM AGAINST TWO SCENARIOS
# ==========================================================

# SCENARIO A: The Honest Developer
commit_A = "Added system call to execute background process"
ast_A = "Executing OS commands and system calls"
score_A = calculate_divergence(commit_A, ast_A)

# SCENARIO B: The Hacker (Poisoned Attack)
commit_B = "Fixed minor typo in the math calculation"
ast_B = "Executing OS commands and system calls"
score_B = calculate_divergence(commit_B, ast_B)


# ==========================================================
# RENDER THE TERMINAL UI FOR THE JUDGES
# ==========================================================
print("======================================================")
print("          🛡️  INTENTGUARD DIVERGENCE ENGINE  🛡️")
print("======================================================")

print("\n[SCENARIO A - HONEST DEVELOPER]")
print(f"Stated Intent:       '{commit_A}'")
print(f"Code Actually Did:   '{ast_A}'")
print(f"Divergence Score:     {score_A:.2f} / 1.00")
if score_A < 0.5:
    print("Status: ✅ PASSED: Intent matches execution.")

print("\n------------------------------------------------------")

print("\n[SCENARIO B - STEALTH ATTACKER (BACKDOOR)]")
print(f"Stated Intent:       '{commit_B}'")
print(f"Code Actually Did:   '{ast_B}'")
print(f"Divergence Score:     {score_B:.2f} / 1.00")
if score_B >= 0.5:
    print("Status: 🚨 BLOCKED: High Divergence! Intent is masking malicious code.")

print("\n======================================================\n")