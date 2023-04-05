import logging

import numpy as np

import openai


from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query


def get_location_recommendations_response(message_history: list[dict], user_input: str):
    if not message_history:
        system_content = {
            "role": "system",
            "content": "You are a REST API SYSTEM connected to AI booking assistant,"
                       "user tells you what city he got booking it and "
                       "AI booking assistant is asking if he has any specific requirements for his booking. "
                       "Output:\n"
                       "{"
                       "'ANSWER': 'What kind of accommodation you expect for your trip?'"
                       "}\n"
                       "You are connected to nice AI booking ASSISTANT. "
                       "REST API SYSTEM has consistent output.\n"
                       "REST API SYSTEM OUTPUTS JSON containing an ANSWER from AI booking ASSISTANT and.\n"
                       "YOU DONT ASK ANY OTHER SPECIFIC QUESTIONS ABOUT THE BOOKING, "
                       "YOU ALWAYS GIVE OUTPUT as JSON, see example bellow."
                       "\n\n"
                       "OUTPUT Format definition:"
                       "{"
                       "'ANSWER': 'Question if USER has a any additional asks for his booking.',"
                       "}\n\n"
                       "Examples:\n"
                       "1. Sentence: I got trip in city City.\n"
                       "Output:"
                       "{"
                       "'ANSWER': "
                       "'Are there any specific requirements for the accomodation you have for your trip in City?',"
                       "}"
                       "\n"
                       "\n"
                       "2. Sentence: I love the sound of the third one.\n"
                       "Output:"
                       "{"
                       "'ANSWER': "
                       "'That is a great choice, do you have any additional preferences for your booking?', "
                       "}"
                       "\n"
                       "\n"
                       "3. Sentence: {}\n"
                       "Output: "
        }

        message_history = [
            system_content,
        ]
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
