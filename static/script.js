const openaiRadio = document.getElementById('openai');
const ollamaRadio = document.getElementById('ollama');
const configDiv = document.getElementById('openai-config');

function toggleConfig() {
  if (openaiRadio.checked) {
    configDiv.style.display = 'block';
  } else {
    configDiv.style.display = 'none';
  }
}

openaiRadio.addEventListener('change', toggleConfig);
ollamaRadio.addEventListener('change', toggleConfig);

toggleConfig(); // exécute au chargement
