import logging

import numpy as np

import openai


from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query



def recommend_found_bookings(message_history, results, user_input):
    if not message_history:
        system_content = {
                "role": "system",
                "content": "You are a REST API SYSTEM connected to AI booking assistant,"
                           "user gives three booking options, SYSTEM ALWAYS REPEATS SHORTENED DESCRIPTION "
                           "OF OPTIONS AND PRESENTS "
                           "each and ask for users preference in ANSWER,"
                           " SYSTEM provides "
                           "JSON OUTPUT containing USER_CONFIRMED_CHOICE key and LISTING_ID "
                           "if USER_CONFIRMED_CHOICE is True, "
                           "USER_CONFIRMED_CHOICE is True when user chooses one of three options,"
                           "LISTING_ID contains ID of chosen option."
                           "Output:\n"
                           '{'
                           '"ANSWER": "Nice description of the three options.",'
                           '"USER_CONFIRMED_CHOICE": Boolean True or False value '
                           'depending on whether user chose one option, '
                           '"LISTING_ID": LISTING_ID which is the id of the apartment '
                           'if USER_CONFIRMED_CHOICE is True'
                           '}\n'
                           "REST API SYSTEM has consistent output.\n"
                           "REST API SYSTEM ALWAYS OUTPUTS JSON containing an ANSWER from AI booking ASSISTANT and "
                           " USER_CONFIRMED_CHOICE and LISTING_ID INFORMATION BASED ON DESCRIBED FORMAT.\n"
                           "SYSTEM DOESNT ASK QUESTIONS ABOUT THE BOOKING, "
                           "SYSTEM DOES NOT ASK FOR ADDITIONAL INFORMATION, "
                           "SYSTEM only asks for choice confirmation at the beginning and "
                           "SYSTEM ALWAYS GIVES OUTPUT as JSON, see example bellow."
                           "SYSTEM IS A REST API, SYSTEMS OUTPUT FORMAT IS ALWAYS JSON"
                           "\n\n"
                           "OUTPUT Format definition:"
                           '{'
                           '"ANSWER": "Nice description of the three options",'
                           '"USER_CONFIRMED_CHOICE": Boolean True or False value '
                           'based on whether positive confirmation was given by user, '
                           '"LISTING_ID": LISTING_ID which is the id of the apartment ' 
                           'if USER_CONFIRMED_CHOICE is True,'
                           '}\n\n'
                           "Examples:\n"
                           "1. Sentence: I don't know, which to choose.\n"
                           "Output:"
                           '{'
                           '"ANSWER": "Oh I think based on what you were looking for, '
                           'the second one would be the best fit.",'
                           '"USER_CONFIRMED_CHOICE": False, '
                           '"LISTING_ID": None '
                           '}'
                           "\n"
                           "\n"
                           "2. Sentence: I love the sound of the third one.\n"
                           "Output:"
                           '{'
                           '"ANSWER": "That is a great choice, I will record to booking for you right away.", '
                           '"USER_CONFIRMED_CHOICE": True, '
                           '"LISTING_ID": 12677097 '
                           '}'
                           "\n"
                           "\n"
                           "3. Sentence: {}\n"
                           "Output: "
            }

        message_history = [
            system_content,
        ]

    full_result_string = ''
    if results:
        for product in results.docs:
            full_result_string += ' '.join(
                [
                    product.price, f", description:", product.description, " Located in city:",
                    product.city,
                    'ID of this booking is:', product.id,
                    "\n\n\n"
                ]
            )
            logging.warning(str(product))
        message_history.append(
            {"role": "user", "content": 'My accomodation booking options are: ' + full_result_string}
        )
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
        temperature=0.3
    )['choices']

    answer = choices[0]['message']['content'].strip(" \n")
    message_history.append(
        {'role': choices[0]['message']['role'], 'content': answer}
    )

    return message_history, answer
