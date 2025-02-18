from listen import Listener
from voice import Voice, Voice2
from openai import OpenAI


class Chatbot:
    def __init__(self):
        self.listener = Listener()
        self.voice = Voice2()
        self.client = OpenAI()
    
    def ask_question(self):
        text = self.listener.listen(5)
        response = self.generate_response(text)
        self.voice.speak(response)
    
    def shutdown(self):
        self.listener.close()
        self.voice.close()
    
    def generate_response(self, input):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Chatbot. Antworte auf Deutsch in kurzen cleveren Antworten. Nutze keine Emojis!"},
                {
                    "role": "user",
                    "content": input
                    },
            ],
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    chatbot = Chatbot()
    running = True
    
    print("Chatbot is ready")
    
    while running:
        print("\nChoose an option:")
        print("1: Ask question")
        print("2: Shutdown")

        option = input("Option: ")
        match option:
            case "1":
                chatbot.ask_question()
            case "2":
                chatbot.shutdown()
                running = False
            case _:
                print("Invalid option")
