import os
import openai

MODEL = 'gpt-3.5-turbo'


openai.api_key = os.environ.get('OPEN_API_KEY')

chatter = openai.ChatCompletion(
    model_name=MODEL,
    verbose=False
)


def get_response(message_history: list[dict], user_input: str):
    if not message_history:
        message_history = [
            {"role": "system", "content": "You are the assistant answering users questions."},
            {"role": "user", "content": user_input}
        ]
    return chatter.create(
          model="gpt-3.5-turbo",
          messages=message_history
    )
