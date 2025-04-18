from flask import request, jsonify
from services.youtube_transcript import get_transcript_text
from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from services.ia_client_factory import get_llm_client
from utils.logger import Logger
from utils.decorators import timed, safe_exec
from services.prompt_builder import build_final_prompt, build_initial_prompt, build_update_prompt
from utils.input_sanitizer import sanitize_form_data
from utils.config import Config
import markdown
from utils.count_tokens import count_tokens
from services.text_splitter import split_transcript_by_tokens
from services.youtube_transcript import get_transcript_text
from utils.dependency_injector import inject_dependencies, inject_logger, inject_config

@inject_logger
def sanitize_user_choices(initial_form_data, logger=None):
    try:
        # 1. Récupération et sanitisation des champs du formulaire
        raw_form_data = {
            "youtube_url": initial_form_data.get("youtube_url", ""),
            "engine": initial_form_data.get("engine", "openai-default"),  # Valeur par défaut : openai-default
            "api_key": initial_form_data.get("api_key", ""),
            "api_url": initial_form_data.get("api_url", ""),
            "summary_type": initial_form_data.get("summary_type", "full"),
            "language": initial_form_data.get("language", "en"),
            "detail_level": initial_form_data.get("detail_level", "medium"),
            "style": initial_form_data.get("style", "mixed"),
            "add_emojis": initial_form_data.get("add_emojis", "yes"),
            "add_tables": initial_form_data.get("add_tables", "yes"),
            "specific_instructions": initial_form_data.get("specific_instructions", "")
        }
        
        # Sanitiser les données du formulaire
        form_data = sanitize_form_data(raw_form_data)
        
        if not form_data["youtube_url"]:
            raise ValueError("URL YouTube invalide. Veuillez fournir une URL valide.")
        
        return form_data

    except Exception as e:
        logger.exception(f"❌ Error sanitizing user choices: {str(e)}")
        raise  

@timed
@inject_dependencies
def summarize(logger=None, config=None):
    try:
        logger.info("🔁 New summarization request received")
        transcript_text = ""
        form_data = sanitize_user_choices(request.form, logger=logger)
        
        # Utiliser directement le moteur IA sélectionné (simplifié)
        engine = form_data["engine"]
        api_key = form_data["api_key"]
        api_url = form_data["api_url"]
        summary_type = form_data["summary_type"]
        language = form_data["language"]
        detail_level = form_data["detail_level"]
        youtube_url = form_data["youtube_url"]

        # Masquer la clé API dans les logs
        masked_api_key = "***" if api_key else ""
        logger.debug(f"URL: {youtube_url} | Engine: {engine} | Type: {summary_type} | Lang: {language} | Detail: {detail_level}")
        logger.info(f"🧠 Appel API avec {engine} | API URL: {api_url if api_url else 'default'} | API Key: {masked_api_key}")

        # 2. Extraction du texte depuis YouTube
      
        try:
            transcript_text = get_transcript_text(youtube_url).replace('\n', ' ')
            logger.debug("✅ Transcript successfully retrieved")
        except ValueError as e:
            return jsonify({
                "summary": f"Erreur : {str(e)}",
                "tokens": {},
                "execution_time": 0
            }), 400
        except Exception as e:
            logger.exception(f"❌ Error retrieving transcript: {str(e)}")
            return jsonify({
                "summary": "Erreur lors de l'extraction du transcript. Vérifiez que la vidéo existe et dispose de sous-titres.",
                "tokens": {},
                "execution_time": 0
            }), 500

        # 3. Sélection du client IA
        logger.info(f"🧠 Calling {engine} with API URL: {api_url}")
        client = get_llm_client(engine, api_url=api_url, api_key=api_key, logger=logger, config=config)

        # 4. Préparation des options pour le prompt
        user_choices = {
            "language": language,
            "detail_level": detail_level,
            "summary_type": summary_type,
            "style": form_data["style"],
            "add_emojis": form_data["add_emojis"],
            "add_tables": form_data["add_tables"],
            "specific_instructions": form_data["specific_instructions"]
        }
        
        # 5. Appels successifs à l'IA
        chunks = split_transcript_by_tokens(transcript_text, max_tokens=config.MAX_TOKENS, 
                                           model=config.OPENAI_ENCODING_MODEL, logger=logger, config=config)
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
        
        # 6. Renvoyer le résultat
        logger.debug("⤵️ RAW Final Summary before markdown conversion")
        html_summary = markdown.markdown(current_summary)
        return jsonify({
            "summary": html_summary,
            "transcript": transcript_text,
            "tokens": response_data.get("tokens_used", {}),
            "execution_time": response_data.get("execution_time", 0)
        })

    except Exception as e:
        logger.exception(f"❌ Error during summarization process: {str(e)}")
        return jsonify({
            "summary": f"Erreur côté serveur : {str(e)}",
            "transcript": transcript_text,
            "tokens": {},
            "execution_time": 0
        }), 500

@inject_logger
def get_transcript_only(logger=None):
    try:
        youtube_url = request.form.get("youtube_url", "")
        if not youtube_url:
            return jsonify({"error": "URL YouTube invalide. Veuillez fournir une URL valide."}), 400
        
        form_data = sanitize_user_choices(request.form, logger=logger)
        youtube_url = form_data["youtube_url"]
        transcript = get_transcript_text(youtube_url)
        return jsonify({"transcript": transcript}), 200

    except ValueError as e:
        logger.exception(f"❌ Error during transcript extraction: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception(f"❌ Error during transcript extraction: {str(e)}")
        return jsonify({"error": str(e)}), 500