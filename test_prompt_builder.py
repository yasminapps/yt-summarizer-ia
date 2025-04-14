from services.prompt_builder import build_final_prompt

fake_transcript = "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."

user_choices = {
    "language": "fr",
    "detail_level": "medium",
    "summary_type": "tools",
    "style": "bullet",
    "add_emojis": "yes",
    "add_tables": "yes",
    "specific_instructions": "Mets les concepts clés en gras."
}

prompt = build_final_prompt(
    transcript=fake_transcript,
    user_choices=user_choices
)

print(prompt)
