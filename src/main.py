from listen import Listener
from voice import speak





def main():
    listener = Listener()
    text = listener.listen(5)
    save_text(text)
    print(f"Recognized text: {text}")
    speak(text)
    
    
def save_text(text):
    with open("temp/text.txt", "w") as file:
        file.write(text)


if __name__ == '__main__':
    main()