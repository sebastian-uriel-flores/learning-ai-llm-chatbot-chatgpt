import openai
import os
import requests
import time

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("TELEGRAM_TOKEN")

def get_updates(offset):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = { "timeout": 100, "offset": offset }
    response = requests.get(url, params=params)
    return response.json()["result"]

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = { "chat_id": chat_id, "text": text }
    response = requests.post(url, params=params)
    return response

def get_openai_response(prompt):
    model_engine = "davinci:ft-sebastian-uriel-flores-2023-11-19-16-42-36"
    
    try:
        response = openai.Completion.create(
            engine = model_engine,
            prompt = prompt,
            max_tokens = 200,
            n = 1,
            stop = " END",
            temperature = 0.8
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Se produjo el error {e}")
        return None

def main():
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                chat_id = update["message"]["chat"]["id"]
                user_message = update["message"].get("text")
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                                
                if (GPT is None):
                    GPT = "Ha ocurrido un error"
                    
                send_message(chat_id, GPT) 
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()