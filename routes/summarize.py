from flask import request, jsonify
from services.youtube_transcript import get_transcript_text
from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from services.ia_client_factory import get_llm_client
from utils.logger import get_logger
from utils.decorators import timed, safe_exec
from services.prompt_builder import build_final_prompt
import markdown


logger = get_logger()

@timed
def summarize():
    try:
        logger.info("🔁 New summarization request received")

        # 1. Récupération des champs du formulaire
        form_data = {
            "youtube_url": request.form.get("youtube_url", "").strip(),
            "engine": request.form.get("engine", "ollama"),
            "ia_source": request.form.get("ia_source", "").strip(),
            "api_key": request.form.get("api_key", "").strip(),
            "api_url": request.form.get("api_url", "").strip(),
            "summary_type": request.form.get("summary_type", "full"),
            "language": request.form.get("language", "en"),
            "detail_level": request.form.get("detail_level", "medium")
        }
        youtube_url = form_data["youtube_url"]
        # Utiliser ia_source s'il est défini, sinon utiliser engine
        engine = form_data["ia_source"] if form_data["ia_source"] else form_data["engine"]
        api_key = form_data["api_key"]
        api_url = form_data["api_url"]
        summary_type = form_data["summary_type"]
        language = form_data["language"]
        detail_level = form_data["detail_level"]

        logger.debug(f"URL: {youtube_url} | Engine: {engine} | Type: {summary_type} | Lang: {language} | Detail: {detail_level}")

        # 2. Extraction du texte depuis YouTube
        transcript_text = get_transcript_text(youtube_url)
        logger.debug("✅ Transcript successfully retrieved")

        # 3. Génération du prompt
        logger.info("🧠 Generating prompt and calling LLM")
        # juste avant de faire client(prompt)
        prompt = build_final_prompt(transcript_text, {
            "language": language,
            "detail_level": detail_level,
            "summary_type": summary_type,
            "style": request.form.get("style", "mixed"),
            "add_emojis": request.form.get("add_emojis", "yes"),
            "add_tables": request.form.get("add_tables", "yes"),
            "specific_instructions": request.form.get("specific_instructions", "").strip()
        })

        # 4. Sélection du client IA
        logger.info(f"🧠 Calling {engine} with API URL: {api_url}")
        client = get_llm_client(engine, api_url=api_url, api_key=api_key)
        response_data = client(prompt)
        execution_time = response_data.get("execution_time", None)
        logger.info("✅ Summary successfully generated")

        # 5. Renvoyer le résultat
        print("⤵️ RAW Summary before markdown:\n", response_data.get("response", "Error"))
        html_summary = markdown.markdown(response_data.get("response", "Error"))
        return jsonify({
            "summary": html_summary,
            "tokens": response_data.get("tokens_used", {}),
            "execution_time": response_data.get("execution_time", 0)
        })

    except Exception as e:
        logger.exception("❌ Error during summarization process")
        return jsonify({
            "summary": f"Erreur côté serveur : {str(e)}",
            "tokens": {},
            "execution_time": 0
        }), 500

