import pyaudio
import wave
import whisper
import time
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"

class Listener:
    def __init__(self, language="de"):
        print("Initializing listener...")
        self.whisper_model = whisper.load_model("large", device=device, in_memory=True)
        self.language = language
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=16000,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        print("Listener initialized")

    def listen(self, duration=5):
        print("Listening...")
        frames = []
        for _ in range(0, int(16000 / self.chunk * duration)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        print("Done listening")
        self.close()
        path_to_wav = frames_to_wav(frames)
        result = self.wav_to_text(path_to_wav)
        return result["text"]
    
    def wav_to_text(self, file_path):
        print("Converting wav to text...")
        text = self.whisper_model.transcribe(file_path, language=self.language)
        print("Done converting")
        return text

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


