import pyaudio


def list_output_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i, dev['name'], dev['maxOutputChannels']))
    p.terminate()
    
list_output_devices()