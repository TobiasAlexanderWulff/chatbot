from TTS.api import TTS


def list_voice_conversion_models():
    conversion_models = list(filter(lambda model: model.startswith("voice_conversion_models/"), TTS().list_models()))
    print(conversion_models)

if __name__ == '__main__':
    list_voice_conversion_models()