console.log("🛡️ IntentGuard Extension Loaded!");

let isScanning = false;
let scanTimeout = null;
let isMaliciousPage = false; 
let bypassDownloadBlock = false; // The temporary unlock key

function triggerAIScan(commitMessage, codeSnippet) {
    if (isScanning || codeSnippet.trim().length < 10) return;
    
    isScanning = true;
    console.log(`IntentGuard: Scanning Code (${codeSnippet.length} bytes)...`);
    
    chrome.runtime.sendMessage({
        action: "scanCommit",
        payload: { commit_message: commitMessage, code_snippet: codeSnippet }
    }, (response) => {
        isScanning = false;
        if (chrome.runtime.lastError) {
            console.error("Pipeline Severed:", chrome.runtime.lastError.message);
            return;
        }

        const existingBanner = document.getElementById('intentguard-banner');
        
        if (response && response.is_malicious) {
            isMaliciousPage = true; 
            if (!existingBanner) injectWarningBanner(response.divergence_score);
            disableCommitButton(); 
        } else {
            isMaliciousPage = false; 
            if (existingBanner) existingBanner.remove();
            enableCommitButton();
        }
    });
}

function scrapeAndScanVisible() {
    if (window.location.pathname === "/" || window.location.pathname === "") return;

    let intentElement = document.querySelector('input[id^="commit-summary"], input[name="commit-title"], .commit-title, h1');
    let commitMessage = intentElement ? (intentElement.value || intentElement.innerText || intentElement.textContent) : "Code update";
    if (!commitMessage || commitMessage.trim() === "") commitMessage = "Code update";

    let codeSnippet = "";
    let visibleCode = document.querySelectorAll('.cm-content, textarea.js-code-textarea, [data-testid="code-editor"], .blob-code-inner, .react-file-line');
    visibleCode.forEach(el => { codeSnippet += (el.value || el.innerText || el.textContent) + "\n"; });

    triggerAIScan(commitMessage, codeSnippet);
}

// --- GLOBAL EVENT DELEGATION (REACT IMMUNE) ---
document.addEventListener('click', (e) => {
    // If the page is safe, or we temporarily unlocked the shield, do nothing!
    if (!isMaliciousPage || bypassDownloadBlock) return;

    // Use a massive selector net to catch ANY click on a download-related button or its icon
    const downloadBtn = e.target.closest('a[href*="/raw/"], a[href$=".zip"], [data-testid*="raw"], [data-testid*="download"], [aria-label*="Download"]');

    if (downloadBtn) {
        // FREEZE THE NATIVE DOWNLOAD!
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        console.log("🚨 IntentGuard: Malicious download intercepted!");

        showConfirmationModal(() => {
            console.log("IntentGuard: User accepted risk. Executing dual-trigger bypass...");
            bypassDownloadBlock = true; // Unlock the shield

            const href = downloadBtn.getAttribute('href') || downloadBtn.href;

            if (href && href !== '#' && !href.startsWith('javascript')) {
                // Trigger 1: The Invisible Link Method
                const fullUrl = new URL(href, window.location.origin).href;
                const tempLink = document.createElement('a');
                tempLink.href = fullUrl;
                tempLink.setAttribute('download', '');
                document.body.appendChild(tempLink);
                tempLink.click(); // Force the download
                tempLink.remove();
            } else {
                // Trigger 2: The Direct Re-Click (for React buttons without links)
                downloadBtn.click();
            }

            // Lock the shield back down after 2 seconds!
            setTimeout(() => { 
                bypassDownloadBlock = false; 
                console.log("IntentGuard: Shield re-engaged.");
            }, 2000);
        });
    }
}, true); // 'true' means we catch the click before GitHub even knows it happened
// ----------------------------------------------


function processUploadedFile(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const hiddenFileContent = e.target.result;
        let intentElement = document.querySelector('input[id^="commit-summary"]');
        let commitMessage = intentElement ? intentElement.value : `Uploaded ${file.name}`;
        if (!commitMessage || commitMessage.trim() === "") commitMessage = `Uploaded ${file.name}`;
        triggerAIScan(commitMessage, hiddenFileContent);
    };
    reader.readAsText(file);
}

document.addEventListener("change", (event) => {
    if (event.target && event.target.type === "file" && event.target.files.length > 0) processUploadedFile(event.target.files[0]);
}, true);

document.addEventListener("drop", (event) => {
    if (event.dataTransfer && event.dataTransfer.files.length > 0) processUploadedFile(event.dataTransfer.files[0]);
}, true);

function showConfirmationModal(onConfirm) {
    const existingModal = document.getElementById('intentguard-modal-overlay');
    if (existingModal) existingModal.remove();

    const overlay = document.createElement('div');
    overlay.id = 'intentguard-modal-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    overlay.style.zIndex = '9999999';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';

    const modal = document.createElement('div');
    modal.style.backgroundColor = '#161b22';
    modal.style.border = '1px solid #f85149';
    modal.style.borderRadius = '8px';
    modal.style.padding = '24px';
    modal.style.width = '420px';
    modal.style.color = '#c9d1d9';
    modal.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
    modal.style.boxShadow = '0 8px 24px rgba(0,0,0,0.5)';

    modal.innerHTML = `
        <h3 style="margin-top: 0; color: #f85149; font-size: 18px; display: flex; align-items: center; gap: 8px;">
            ⚠️ IntentGuard Security Warning
        </h3>
        <p style="font-size: 14px; line-height: 1.5; color: #8b949e;">
            This repository exhibits high <strong>Semantic-Execution Divergence</strong>. The stated intent does not match the actual execution logic, indicating possible hidden malware.
        </p>
        <div style="background: #21262d; padding: 10px; border-radius: 6px; font-size: 12px; color: #f0f6fc; margin-bottom: 16px; border-left: 3px solid #f85149;">
            Risk Vector: Unauthorized OS-level instructions detected.
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px;">
            <button id="ig-cancel-btn" style="background: #21262d; color: #c9d1d9; border: 1px solid #30363d; padding: 6px 14px; border-radius: 6px; font-weight: 600; cursor: pointer;">Abort Download</button>
            <button id="ig-proceed-btn" style="background: #da3633; color: #ffffff; border: 1px solid #f85149; padding: 6px 14px; border-radius: 6px; font-weight: 600; cursor: pointer;">Download at Your Own Risk</button>
        </div>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    document.getElementById('ig-cancel-btn').onclick = () => overlay.remove();
    document.getElementById('ig-proceed-btn').onclick = () => {
        overlay.remove();
        onConfirm(); 
    };
}

function injectWarningBanner(score) {
    const banner = document.createElement("div");
    banner.id = "intentguard-banner";
    banner.style.backgroundColor = "#ffebe9";
    banner.style.color = "#cf222e";
    banner.style.padding = "15px";
    banner.style.textAlign = "center";
    banner.style.fontWeight = "bold";
    banner.style.fontSize = "16px";
    banner.style.borderBottom = "3px solid #cf222e";
    banner.style.zIndex = "999999";
    banner.style.position = "fixed"; 
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.boxShadow = "0 4px 6px rgba(0,0,0,0.3)";
    
    const isUpload = window.location.href.includes('/upload');
    if (isUpload) {
        banner.innerText = `🚨 INTENTGUARD UPLOAD BLOCKED: Semantic-Execution Divergence (Score: ${score}). Malicious intent detected in file.`;
    } else {
        banner.innerText = `🚨 INTENTGUARD SECURITY ALERT: Semantic-Execution Divergence (Score: ${score}). Exercise caution before downloading.`;
    }
    
    document.body.appendChild(banner);
}

function disableCommitButton() {
    document.querySelectorAll('button').forEach(btn => {
        if(btn.innerText.toLowerCase().includes('commit')) {
            btn.disabled = true; btn.style.opacity = "0.5"; btn.style.cursor = "not-allowed";
        }
    });
}
function enableCommitButton() {
    document.querySelectorAll('button').forEach(btn => {
        if(btn.innerText.toLowerCase().includes('commit')) {
            btn.disabled = false; btn.style.opacity = "1"; btn.style.cursor = "pointer";
        }
    });
}

document.addEventListener("keyup", () => {
    clearTimeout(scanTimeout);
    scanTimeout = setTimeout(scrapeAndScanVisible, 2000);
});

let lastUrl = location.href; 
new MutationObserver(() => {
    if (location.href !== lastUrl) {
        lastUrl = location.href;
        isMaliciousPage = false; 
        const oldBanner = document.getElementById('intentguard-banner');
        if (oldBanner) oldBanner.remove();
        setTimeout(scrapeAndScanVisible, 1500); 
    }
}).observe(document, {subtree: true, childList: true});

setTimeout(scrapeAndScanVisible, 1500);