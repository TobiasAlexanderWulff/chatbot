import torch
import os
from TTS.api import TTS


text = "Das ist ein Testsatz. Er wird von einer künstlichen Intelligenz in Sprache umgewandelt. Die Sprache ist Deutsch."
language = "de"


device = "cuda" if torch.cuda.is_available() else "cpu"

speakers = list(filter(lambda model: model.startswith(f"tts_models/{language}"), TTS().list_models()))
print(speakers)

if not os.path.exists("out"):
    os.makedirs("out")

if not os.path.exists(f"out/{language}"):
    os.makedirs(f"out/{language}")

for speaker in speakers:
    tts = TTS(speaker).to(device)
    speaker_str = speaker.replace(f"tts_models/{language}_", "").replace("/", "_")
    tts.tts_to_file(text=text, file_path=f"out/{language}/test_" + speaker_str + ".wav")

