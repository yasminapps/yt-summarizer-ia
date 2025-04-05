# test_local_transcript.py (à côté)
from services.youtube_transcript import get_transcript_text
from utils.formatter import clean_transcript

url="https://www.youtube.com/watch?v=MOlO1_mj1dU&list=PLlOtFRvZOw6x4q8f0pd68xLpY7otMhs9l&index=6"
# Étape 1 : récupération du transcript brut
raw_text = get_transcript_text(url)
print("Transcript brut (début) :")
print(raw_text[:500], "\n...")

# Étape 2 : nettoyage avec clean_transcript
cleaned_text = clean_transcript(raw_text)
print("\nTranscript nettoyé :")
print(cleaned_text, "\n...")


