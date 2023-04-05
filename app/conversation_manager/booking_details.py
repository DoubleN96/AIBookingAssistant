import logging

import numpy as np

import openai


from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query

def ask_for_booking_details(message_history: list[dict], user_input: str, booking_known_info: dict):
    if booking_known_info:
        known = list(booking_known_info.keys())
    else:
        known = []

    if not message_history:
        system_content = {
                "role": "system",
                "content": "User is asking to book a room and you are "
                           "generic company room or apartment booking ASSISTANT "
                           "asking USER for information to make the booking,"
            }

        needed_entities = [
            ent_name for ent_name in ['FULL_NAME', 'DATES', 'CITY', 'BUDGET', 'GUEST_COUNT'] if ent_name not in known
        ]

        system_content['content'] += (
            f"ONLY ask him nicely for these information on `{', '.join(needed_entities)}`for his booking."
            f"You ask ONLY about: `{', '.join(needed_entities)}`"
        )
        message_history = [
            system_content,
            {"role": "user", "content": user_input}
        ]
    else:
        message_history.append(
            {"role": "user", "content": user_input}
        )

    choices = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )['choices']

    message_history.append(
        {'role': choices[0]['message']['role'], 'content': choices[0]['message']['content'].strip(" \n")}
    )

    return choices[0]['message']['content'].strip(" \n"), message_history
