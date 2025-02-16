import pyaudio
import wave
import whisper
import torch
import numpy as np


device = "cuda" if torch.cuda.is_available() else "cpu"

class Listener:
    def __init__(self, language="de"):
        print("Initializing listener...")
        self.whisper_model = whisper.load_model("large", device=device, in_memory=True)
        self.language = language
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        print("Listener initialized")

    def listen(self, duration=5):
        print("Listening...")
        self.stream = self.p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True,
                          frames_per_buffer=self.chunk)
        frames = []
        for _ in range(0, int(16000 / self.chunk * duration)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        print("Done listening")
        
        audio_bytes = b"".join(frames)
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        audio_np /= 32768.0  # Normierung auf [-1, 1]
        
        result = self.whisper_model.transcribe(audio_np, language=self.language) # Speach to text
        
        return result["text"]
    


    def close(self):
        print("Closing listener...")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("Listener closed")


def frames_to_wav(frames):
    print("Saving as wav...")
    file_path = "temp/recording.wav"
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Saved as wav")
    return file_path

if __name__ == '__main__':
    listener = Listener()
    text = listener.listen()
    print(text)


