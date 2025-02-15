import torch
import os
from TTS.api import TTS


device = "cuda" if torch.cuda.is_available() else "cpu"

# print(TTS().list_models())

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

if not os.path.exists("out"):
  os.makedirs("out")
  
if not os.path.exists("out/voice_samples"):
  os.makedirs("out/voice_samples")

for speaker in tts.speakers:
    tts.tts_to_file(
      text="Hello world!",
      speaker=speaker,
      language="en",
      file_path=f"out/voice_samples/{speaker}.wav"
    )


