from listen import Listener
from voice import speak
from openai import OpenAI
import time





def main():
    
    start_time = time.time()
    
    # TODO implment some kind of logging
    
    listener = Listener()
    text = listener.listen(5)
    
    after_listen_time = time.time()
    print(f"Listening took {after_listen_time - start_time} seconds")
    time_without_listening_duration = after_listen_time - 5
    print(f"Time without listening duration: {time_without_listening_duration} seconds")
    
    
    save_text(text)
    print(f"Recognized text: {text}")
    
    response = generate_response(text)
    
    speak(response)
    
    
def save_text(text):
    with open("temp/text.txt", "w") as file:
        file.write(text)
        

def generate_response(text):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Chatbot. Antworte auf Deutsch in kurzen cleveren Antworten. Nutze keine Emojis!"},
            {
                "role": "user",
                "content": text
                },
        ],
    )
    return completion.choices[0].message.content


if __name__ == '__main__':
    main()