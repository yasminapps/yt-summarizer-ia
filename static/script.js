window.onload = function() {
    // 🌐 Détection automatique de la langue du navigateur
    const userLang = navigator.language || navigator.userLanguage;
    const langCode = userLang.split('-')[0];
    const languageInput = document.getElementById("language");
    if (languageInput && !languageInput.value) {
        languageInput.value = langCode;
    }

    // 🧠 Affichage dynamique de la config OpenAI
    const openaiRadio = document.getElementById('openai');
    const ollamaRadio = document.getElementById('ollama');
    const configDiv = document.getElementById('openai-config');

    function toggleConfig() {
        if (openaiRadio && openaiRadio.checked) {
            configDiv.style.display = 'block';
        } else {
            configDiv.style.display = 'none';
        }
    }

    if (openaiRadio && ollamaRadio && configDiv) {
        openaiRadio.addEventListener('change', toggleConfig);
        ollamaRadio.addEventListener('change', toggleConfig);
        toggleConfig(); // exécute au démarrage
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const summaryResult = document.getElementById("summary-result");
    const errorMessage = document.getElementById("error-message");
    const tokenInfo = document.getElementById("token-info");

    const loadingAnimation = document.getElementById("loading-animation");
    const loadingDots = document.getElementById("loading-dots");
    let dotInterval = null;

    function startLoadingAnimation() {
        summaryResult.textContent = "⏳ Generating summary";
        loadingAnimation.style.display = "flex";
        let dots = "";
        dotInterval = setInterval(() => {
            dots = dots.length < 3 ? dots + "." : "";
            loadingDots.textContent = dots;
        }, 500);
    }

    function stopLoadingAnimation() {
        clearInterval(dotInterval);
        loadingAnimation.style.display = "none";
        loadingDots.textContent = "";
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // block default form submission

        // Reset display
        summaryResult.textContent = "";
        errorMessage.textContent = "";
        tokenInfo.textContent = "";

        const formData = new FormData(form);

        startLoadingAnimation();

        try {
            const response = await fetch("/summarize", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            stopLoadingAnimation();

            if (response.ok) {
                summaryResult.textContent = data.summary;
                if (data.tokens && Object.keys(data.tokens).length > 0) {
                    tokenInfo.textContent = `  Tokens used: ${JSON.stringify(data.tokens)}`;
                }
            } else {
                errorMessage.textContent = data.summary || "️⚠️ An error occurred.";
            }
        } catch (err) {
            stopLoadingAnimation();
            errorMessage.textContent = "🚨 Server not reachable or invalid response.";
        }
    });
});
