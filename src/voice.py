import os
import sys
import torch
from TTS.api import TTS
import pyaudio
import wave


test_text = "Hello, this is a test of the TTS system."
test_text_de = "Hallo, dies ist ein Test des TTS-Systems."

speaker = "tts_models/de/thorsten/tacotron2-DDC"

device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    tts = TTS(speaker).to(device)
except FileNotFoundError:
    print("Speaker not found")
    exit(1)
    
p = pyaudio.PyAudio()
    
if not os.path.exists("temp"):
        os.makedirs("temp")


def synthesize(text):
    print("Synthesizing...")
    target_path = f"temp/synth.wav"
    tts.tts_to_file(text=text, file_path=target_path)
    print("Synthesized")
    return target_path


def play(file_path):
    chunk = 1024

    try:
        wf = wave.open(file_path, 'rb')
    except FileNotFoundError:
        print("File not found")
        exit(1)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=0)

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()


def speak(string):
    print("Speaking...")
    print(string)
    play(synthesize(string))
    print("Finished speaking")


if __name__ == "__main__":  
    speak(string=test_text_de)
    
