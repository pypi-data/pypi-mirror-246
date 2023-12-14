import whisper
import sys
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json

speech_file=sys.argv[1]

with Progress(
    TextColumn("🤗 [progress.description]"),
    BarColumn(style="yellow1", pulse_style="white"),
    TimeElapsedColumn(),
) as progress:
    progress.add_task("[yellow]Transcribing...", total=None)
    # text = whisper.transcribe(speech_file)["text"] ## only for debug
    text = whisper.transcribe(speech_file)
    print(text)
    with open("out.json", "w", encoding="utf8") as fp:
        json.dump(text, fp, ensure_ascii=False)
    print(
        f"Voila!✨ Your file has been transcribed go check it out over here 👉 out.json"
    )