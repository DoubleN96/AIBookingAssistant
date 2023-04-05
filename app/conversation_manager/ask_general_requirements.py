import logging

import numpy as np

import openai


from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query

def ask_about_general_requirements_response(message_history: list[dict], user_input: str):
    if not message_history:
        message_history = [
            {
                "role": "system",
                "content": "You are the booking assistant answering touristy questions about "
                           "the city user booked his booking at. "
                           "Start conversation by asking User if he wants to ask for "
                           "recommendations of what to do and see in City of his booking."
            },
            {"role": "user", "content": user_input}
        ]
    else:
        message_history.append(
            {
                'role': 'user',
                'content': user_input
            }
        )

    choices = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature=0.4
    )['choices']

    answer = choices[0]['message']['content'].strip(" \n")
    message_history.append(
        {'role': choices[0]['message']['role'], 'content': answer}
    )

    return message_history, answer
