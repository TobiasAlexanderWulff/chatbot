import os
import torch
from TTS.api import TTS
import pyaudio
import wave
from openai import OpenAI


test_text = "Hello, this is a test of the TTS system."
test_text_de = "Hallo, dies ist ein Test des TTS-Systems."

speaker = "tts_models/de/thorsten/tacotron2-DDC"

device = "cuda" if torch.cuda.is_available() else "cpu"


class Voice:
    def __init__(self):
        try:
            self.tts = TTS(speaker).to(device)
        except FileNotFoundError:
            print("Speaker not found")
            exit(1)
        
        self.p = pyaudio.PyAudio()
        
        if not os.path.exists("temp"):
            os.makedirs("temp")
    
    def synthesize(self, text):
        target_path = f"temp/synth.wav"
        self.tts.tts_to_file(text=text, file_path=target_path)
        return target_path
    
    def play(self, file_path):
        chunk = 1024
        try:
            wf = wave.open(file_path, 'rb')
        except FileNotFoundError:
            print("File not found")
            exit(1)
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
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

    
    def speak(self, string):
        print(f"Chatbot: {string}")
        self.play(self.synthesize(string))
    
    def close(self):
        self.p.terminate()



class Voice2:
    def __init__(self):
        self.client = OpenAI()
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        self.channels = 1
        
        self.silence = chr(0)*self.chunk*self.channels*2 
        
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
    def synthesize(self, text):
        target_path = f"temp/synth.wav"
        
        #with self.client.with_streaming_response.audio.speech.create(
        #    model="tts-1",
        #    voice="alloy",
        #    input=text,
        #) as response:
        #    response.stream_to_file(target_path)
        
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",
            input=text,
            response_format="wav"
        )
        response.write_to_file(target_path)
        
        return target_path
    
    def play(self, file_path):
        chunk = 1024
        try:
            wf = wave.open(file_path, 'rb')
        except FileNotFoundError:
            print("File not found")
            exit(1)
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
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
        
    def play_while_synthesizing(self, text):
        with self.client.with_streaming_response.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            response_format="wav"
        ) as response:
            chunk = 1024
            stream = self.p.open(format=8,
                            channels=1,
                            rate=24000,
                            output=True,
                            output_device_index=0)
            for i, data in enumerate(response.iter_bytes(chunk)):
                if data == '':
                    data = self.silence
                if i == 0:
                    continue
                stream.write(data)
            stream.stop_stream()
            stream.close()
        
    def speak(self, string):
        print(f"Chatbot: {string}")
        #self.play(self.synthesize(string))
        self.play_while_synthesizing(string)
    
    def close(self):
        self.p.terminate()
        



if __name__ == "__main__":  
    voice = Voice2()
    voice.speak(test_text_de)
    voice.close()
    
