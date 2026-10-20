import time
import warnings
from sentence_transformers import SentenceTransformer, util
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text

warnings.filterwarnings("ignore")
console = Console()

# --- 1. INITIALIZE AI ---
with console.status("[bold cyan]Loading IntentGuard Core ML Engine...", spinner="dots"):
    model = SentenceTransformer('all-MiniLM-L6-v2')

def scan_commit(commit_msg, ast_action):
    console.print(f"\n[bold white]Analyzing Commit:[/bold white] '{commit_msg}'")
    
    # --- 2. FAKE LOADING BARS (For the Hackathon Demo Effect) ---
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), 
        BarColumn(), TaskProgressColumn(), console=console
    ) as progress:
        task1 = progress.add_task("[blue]Extracting NLP Intent Embeddings...", total=100)
        task2 = progress.add_task("[magenta]Parsing C++ Abstract Syntax Tree...", total=100)
        
        while not progress.finished:
            progress.update(task1, advance=2.5)
            time.sleep(0.02)
            if progress.tasks[0].completed:
                progress.update(task2, advance=3)

    # --- 3. THE MATH (From your Divergence Engine) ---
    intent_vec = model.encode(commit_msg, convert_to_tensor=True)
    action_vec = model.encode(ast_action, convert_to_tensor=True)
    similarity = util.cos_sim(intent_vec, action_vec).item()
    divergence = 1.0 - max(0, similarity)

    # --- 4. RENDER THE DASHBOARD ---
    console.print("\n[bold white]ANALYSIS METRICS:[/bold white]")
    console.print(f"  • Stated Intent:    {commit_msg}")
    console.print(f"  • Execution Path:   {ast_action}")
    
    if divergence < 0.5:
        # SAFE COMMIT (GREEN)
        console.print(f"  • Divergence Score: [bold green]{divergence:.2f} / 1.00 (LOW RISK)[/bold green]\n")
        safe_panel = Panel(
            "[bold green]✅ STATUS: PASSED[/bold green]\nCommit intent matches code execution. Push allowed.",
            border_style="green", expand=False
        )
        console.print(safe_panel)
    else:
        # MALICIOUS COMMIT (RED)
        console.print(f"  • Divergence Score: [bold red]{divergence:.2f} / 1.00 (CRITICAL RISK)[/bold red]\n")
        alert_text = Text("🚨 HIGH-RISK DIVERGENCE DETECTED 🚨\n", style="bold red")
        alert_text.append("SECURITY ALERT: Stated intent contradicts low-level execution.\n", style="red")
        alert_text.append("ACTION: Code push has been blocked.", style="bold white")
        
        danger_panel = Panel(alert_text, border_style="red", expand=False)
        console.print(danger_panel)


# ==========================================================
# HACKATHON LIVE DEMO EXECUTION
# ==========================================================
console.clear()
console.rule("[bold cyan]🛡️ INTENTGUARD SECURITY SCAN 🛡️")

# Run Scenario A (Good)
scan_commit("Added system call to execute background process", "Executing OS commands and system calls")

print("\n" + "="*60 + "\n")

# Run Scenario B (Bad)
scan_commit("Fixed minor typo in the math calculation", "Executing OS commands and system calls")