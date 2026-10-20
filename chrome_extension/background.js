chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanCommit") {
        console.log("Routing live data to IntentGuard API...");
        
        // The real AI connection
        fetch("http://127.0.0.1:8000/scan", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(request.payload)
        })
        .then(response => {
            if (!response.ok) throw new Error("Server rejected request");
            return response.json();
        })
        .then(data => {
            console.log("AI Server Responded:", data);
            sendResponse(data);
        })
        .catch(error => {
            console.error("AI Connection Failed:", error.message);
            // If the server is off, gracefully fail without breaking GitHub
            sendResponse({ error: error.message, is_malicious: false });
        });
        
        return true; // Keep message channel open
    }
});