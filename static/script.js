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
