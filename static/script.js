window.onload = function() {
    // 🌐 Détection automatique de la langue du navigateur
    const userLang = navigator.language || navigator.userLanguage;
    const langCode = userLang.split('-')[0];
    const languageInput = document.getElementById("language");
    if (languageInput && !languageInput.value) {
        languageInput.value = langCode;
    }

    // 🧠 Affichage dynamique de la config OpenAI
    const engineRadios = document.querySelectorAll('input[name="engine"]');
    const configDiv = document.getElementById('openai-config');

    function toggleConfig() {
        const selected = document.querySelector('input[name="engine"]:checked');
        if (selected && selected.value === 'openai-user') {
            configDiv.style.display = 'block';
        } else {
            configDiv.style.display = 'none';
            document.getElementById("api_url").value = "";
            document.getElementById("api_key").value = "";
        }
    }

    if (engineRadios.length && configDiv) {
        engineRadios.forEach(radio => {
            radio.addEventListener('change', toggleConfig);
        });
        toggleConfig(); // Appel initial
    }
};

// Exposer les fonctions pour les tests
window.formatSecondsToMinutes = function(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(0)}s`;
};

window.startLoadingAnimation = function() {
    const loadingAnimation = document.getElementById("loading-animation");
    const loadingDots = document.getElementById("loading-dots");
    loadingAnimation.style.display = "flex";
    let dots = "";
    window.dotInterval = setInterval(() => {
        dots = dots.length < 3 ? dots + "." : ".";
        loadingDots.textContent = dots;
    }, 500);
};

window.stopLoadingAnimation = function() {
    const loadingAnimation = document.getElementById("loading-animation");
    const loadingDots = document.getElementById("loading-dots");
    clearInterval(window.dotInterval);
    loadingAnimation.style.display = "none";
    loadingDots.textContent = "";
};

window.downloadSummary = function() {
    const text = document.getElementById("summary-result").innerText;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "summary.txt";
    link.click();

    // Vérifier si la méthode existe (peut être absent dans l'environnement de test)
    if (URL.revokeObjectURL) {
        URL.revokeObjectURL(url);
    }
};

window.copySummary = function() {
    const text = document.getElementById("summary-result").innerText;
    return navigator.clipboard.writeText(text).then(() => {
        showCopyFeedback("✅ Summary copied!");
    }).catch(() => {
        showCopyFeedback("❌ Copy failed.");
    });
};

window.downloadTranscript = function() {
    const text = window.lastTranscript || "Transcript unavailable.";
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "transcript.txt";
    link.click();

    // Vérifier si la méthode existe (peut être absent dans l'environnement de test)
    if (URL.revokeObjectURL) {
        URL.revokeObjectURL(url);
    }
};

window.copyTranscript = function() {
    const text = window.lastTranscript || "Transcript unavailable.";
    return navigator.clipboard.writeText(text).then(() => {
        showCopyFeedback("✅ Transcript copied!");
    }).catch(() => {
        showCopyFeedback("❌ Copy failed.");
    });
};

function showCopyFeedback(message) {
    const feedback = document.getElementById("copy-feedback");
    feedback.textContent = message;
    setTimeout(() => feedback.textContent = "", 2000);
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const summaryResult = document.getElementById("summary-result");
    const errorMessage = document.getElementById("error-message");
    const tokenInfo = document.getElementById("token-info");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // block default form submission
        const actionUrl = e.submitter.formAction;
        // Reset display
        summaryResult.innerHTML = "";
        errorMessage.textContent = "";
        tokenInfo.textContent = "";
        const formData = new FormData(form);
        document.getElementById("summary-actions").style.display = "none";
        document.getElementById("transcript-actions").style.display = "none";   
        document.getElementById("summary-container").style.display = "block";
        window.startLoadingAnimation();

        try {
            const response = await fetch(actionUrl, {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            const executionTime = data.execution_time || 0;  // en secondes
           
            window.stopLoadingAnimation();

            if (response.ok) {
                summaryResult.innerHTML = ""  
             
                if (data.summary) {
                    window.lastTranscript = data.transcript;
                    summaryResult.innerHTML = data.summary;
                    summaryResult.style.whiteSpace = "normal";
                    document.getElementById("summary-actions").style.display = "block";
                    document.getElementById("transcript-actions").style.display = "block";
                }

                if (data.transcript) {
                    window.lastTranscript = data.transcript;
                    summaryResult.style.whiteSpace = "pre-wrap";
                    document.getElementById("transcript-actions").style.display = "block";
                }

                if (data.tokens && Object.keys(data.tokens).length > 0) {
                    const totalTokens = data.tokens.total_tokens || "N/A";
                    tokenInfo.textContent = `Tokens used : ${totalTokens}`;
                }
                if (executionTime) {
                    const formattedTime = window.formatSecondsToMinutes(executionTime);
                    tokenInfo.textContent += ` | Execution time: ${formattedTime}`;
                }
            } else {
                errorMessage.textContent = data.summary || "️⚠️ An error occurred.";
            }
        } catch (err) {
            window.stopLoadingAnimation();
            errorMessage.textContent = "🚨 Server not reachable or invalid response.";
        }
    });
});

