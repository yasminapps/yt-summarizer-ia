from flask import request, jsonify
from services.youtube_transcript import get_transcript_text
from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from services.ia_client_factory import get_llm_client
from utils.logger import get_logger
from utils.decorators import timed, safe_exec
from services.prompt_builder import build_final_prompt
import markdown
from utils.count_tokens import count_tokens
from services.text_splitter import split_transcript_by_tokens
from services.text_splitter import split_transcript_by_tokens
from services.prompt_builder import build_initial_prompt, build_update_prompt



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

        # 3. Sélection du client IA
        logger.info(f"🧠 Calling {engine} with API URL: {api_url}")
        client = get_llm_client(engine, api_url=api_url, api_key=api_key)

        # 5. Appels successifs à l'IA
        user_choices = {
            "language": language,
            "detail_level": detail_level,
            "summary_type": summary_type,
            "style": request.form.get("style", "mixed"),
            "add_emojis": request.form.get("add_emojis", "yes"),
            "add_tables": request.form.get("add_tables", "yes"),
            "specific_instructions": request.form.get("specific_instructions", "").strip()
        }
        
        chunks = split_transcript_by_tokens(transcript_text, max_tokens=20000, model="gpt-4o")
        logger.debug(f"✂️ Transcript split into {len(chunks)} parts")

        current_summary = None
        for idx, chunk in enumerate(chunks):
            logger.info(f"🧩 Processing chunk {idx + 1}/{len(chunks)}")

            if idx == 0:
                prompt = build_initial_prompt(chunk, user_choices)
            else:
                prompt = build_update_prompt(chunk, current_summary, idx + 1, user_choices)
                
            response_data = client(prompt)
            current_summary = response_data.get("response", "Error")
        
       
        # 5. Renvoyer le résultat
        print("⤵️ RAW Final Summary before markdown:\n", current_summary)
        html_summary = markdown.markdown(current_summary)
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

