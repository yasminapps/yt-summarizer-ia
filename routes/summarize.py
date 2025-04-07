Pourquoi ai-je reçu deux fois les mêmes logs en si peu de temps ?from flask import request, jsonify
from services.youtube_transcript import get_transcript_text
from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from services.ia_client_factory import get_llm_client
from utils.logger import get_logger

logger = get_logger()

def summarize():
    try:
        logger.info("🔁 New summarization request received")

        # 1. Récupération des champs du formulaire
        youtube_url = request.form.get("youtube_url", "").strip()
        ia_source = request.form.get("ia_source", "ollama")
        api_key = request.form.get("api_key", "").strip()
        api_url = request.form.get("api_url", "").strip()
        summary_type = request.form.get("summary_type", "full")
        language = request.form.get("language", "en")
        detail_level = request.form.get("detail_level", "medium")

        logger.debug(f"URL: {youtube_url} | Engine: {ia_source} | Type: {summary_type} | Lang: {language} | Detail: {detail_level}")

        # 2. Extraction du texte depuis YouTube
        transcript_text = get_transcript_text(youtube_url)
        logger.debug("✅ Transcript successfully retrieved")

        # 3. Génération du prompt
        logger.info("🧠 Generating prompt and calling LLM")
        prompt = f"""
You are an assistant summarizer.

Please generate a {summary_type} summary in {language}, with detail level: {detail_level}.
Transcript:
{transcript_text}
        """.strip()

        # 4. Sélection du client IA
        client = get_llm_client(ia_source, api_url=api_url, api_key=api_key)
        response_data = client(prompt)
        logger.info("✅ Summary successfully generated")

        # 5. Renvoyer le résultat
        return jsonify({
            "summary": response_data.get("response", "Error"),
            "tokens": response_data.get("tokens_used", {})
        })

    except Exception as e:
        logger.exception("❌ Error during summarization process")
        return jsonify({
            "summary": f"Erreur côté serveur : {str(e)}",
            "tokens": {}
        }), 500

