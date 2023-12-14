import whisper
import sys
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json

# speech_file=sys.argv[1]


# text = whisper.transcribe(speech_file)["text"] ## only for debug
text = whisper.transcribe(sys.argv[1])
print(text)
with open("out.json", "w", encoding="utf8") as fp:
    json.dump(text, fp, ensure_ascii=False)
print(
    f"Voila!✨ Your file has been transcribed go check it out over here 👉 out.json"
)