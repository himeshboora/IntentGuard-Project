import sys
import subprocess
import warnings
from sentence_transformers import SentenceTransformer, util
from rich.console import Console
from rich.panel import Panel

warnings.filterwarnings("ignore")
console = Console()

# 1. READ THE LIVE COMMIT MESSAGE
# Git automatically passes the commit message file path as the first argument (sys.argv[1])
commit_msg_file = sys.argv[1]
with open(commit_msg_file, 'r') as f:
    commit_msg = f.read().strip()

# 2. READ THE LIVE CODE DIFF
# We use subprocess to read exactly what C++ code the user staged for this commit
try:
    live_diff = subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
except Exception:
    live_diff = ""

# 3. LIVE AST EXTRACTION (Simplified for this interface test)
ast_action = "Standard code updates"
if "system(" in live_diff or "exec(" in live_diff or "socket(" in live_diff:
    ast_action = "Executing OS commands and system calls"

# 4. RUN THE ML ENGINE
with console.status("[bold cyan]IntentGuard AI analyzing live commit...", spinner="dots"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    intent_vec = model.encode(commit_msg, convert_to_tensor=True)
    action_vec = model.encode(ast_action, convert_to_tensor=True)
    
    similarity = util.cos_sim(intent_vec, action_vec).item()
    divergence = 1.0 - max(0, similarity)

# 5. THE VERDICT (Block or Allow)
console.print("\n[bold white]ANALYSIS METRICS:[/bold white]")
console.print(f"  • Stated Intent:  '{commit_msg}'")
console.print(f"  • Live AST Check: '{ast_action}'")

if divergence >= 0.5:
    console.print(Panel(f"🚨 [bold red]COMMIT BLOCKED (Score: {divergence:.2f})[/bold red]\nSemantic Divergence is too high. You are attempting to mask OS-level system calls behind benign text.", border_style="red"))
    # sys.exit(1) tells Git to ABORT and DESTROY the commit
    sys.exit(1) 
else:
    console.print(Panel(f"✅ [bold green]COMMIT ALLOWED (Score: {divergence:.2f})[/bold green]\nCode execution matches stated intent.", border_style="green"))
    # sys.exit(0) tells Git to SAVE the commit
    sys.exit(0)