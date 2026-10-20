from sentence_transformers import SentenceTransformer
import warnings

# Suppress annoying loading warnings to keep the terminal clean
warnings.filterwarnings("ignore")

# 1. Load a lightweight, pre-trained NLP model
print("Loading NLP Model (This may take a few seconds the first time)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define our test commit messages
commit_1 = "Fixed minor typo in the math calculation"
commit_2 = "Secretly added a reverse shell to steal passwords"

# 3. Convert the English text into mathematical vectors (Embeddings)
print("Converting human intent into mathematical vectors...\n")
vector_1 = model.encode(commit_1)
vector_2 = model.encode(commit_2)

# 4. Display the results
print("======================================================")
print("Commit 1: 'Fixed minor typo in the math calculation'")
print(f"Mathematical Representation: {vector_1[:5]} ... (384 numbers total)")
print("======================================================\n")

print("======================================================")
print("Commit 2: 'Secretly added a reverse shell to steal passwords'")
print(f"Mathematical Representation: {vector_2[:5]} ... (384 numbers total)")
print("======================================================")