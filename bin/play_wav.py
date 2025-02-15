import pyaudio
import wave


chunk = 1024

try:
    wf = wave.open('out/de/test_tts_models_de_thorsten_tacotron2-DDC.wav', 'rb')
except FileNotFoundError:
    print("File not found")
    exit(1)

p = pyaudio.PyAudio()

# List available output devices
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev['name'], dev['maxOutputChannels']))

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
