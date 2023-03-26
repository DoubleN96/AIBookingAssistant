import logging

import numpy as np

import openai

from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query


def recommend_booking(
        message_history,
        user_input: str,
        interaction_count: int,
        booking_chain,
        context_entities: dict,
        redis_connector
):
    interaction_count += + 1
    logging.warning(interaction_count)
    if interaction_count == 1:
        # Run the chain only specifying the input variable.
        keywords = booking_chain.run(
            user_input + ', in city: ' + context_entities['CITY'] + ', these are reservation specification: ' + str(context_entities)
        )
        print(user_input + ', in city: ' + context_entities['CITY'] + ', these are reservation specification: ' + str(context_entities))
        print(keywords)

        top_k = 3
        # vectorize the query
        query_vector = vectorizer.encode(keywords).astype(np.float32).tobytes()
        params_dict = {"vec_param": query_vector}

        # Execute the query
        results = redis_connector.ft().search(get_booking_query(top_k), query_params=params_dict)
        logging.warning(results)
    else:
        results = {}

    message_history, answer, confirmed = recommend_found_bookings(
        message_history,
        results, user_input + ', specification of booking requirements: ' + str(context_entities)
    )
    return message_history, answer, interaction_count, confirmed


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

    choices = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )['choices']

    message_history.append(
        {'role': choices[0]['message']['role'], 'content': choices[0]['message']['content'].strip(" \n")}
    )

    return choices[0]['message']['content'].strip(" \n"), message_history


def recommend_found_bookings(message_history, results, user_input):
    if not message_history:
        system_content = {
                "role": "system",
                "content": "You are a generic company room/apartment booking ASSISTANT. "
                           "Be kind, detailed and try to sell and present one of these three offers "
                           "for the booking of a room or apartment to user. "
                           "Present the three options in a nice way and ask user to choose one. "
                           "YOU DONT ASK QUESTIONS ABOUT THE BOOKING, YOU DO NOT ASK FOR ADDITIONAL INFORMATION, "
                           "YOU only ask to choose one OPTION and then OUTPUT answer as example bellow."
                           "AFTER CHOICE WAS MADE ONLY THANK FOR BOOKING AND GIVE LISTING ID."
                           "\n\n\n"
                           "Output Format:\n"
                           "Nice description of the three options"
                           "----------------"
                           "{"
                           "{"
                           "'USER_CONFIRMED_CHOICE': Boolean True or False value, "
                           "'LISTING_ID': LISTING_ID which, id of the apartment if USER_CONFIRMED_CHOICE is True, "
                           "}"
                           "}"
                           "}\n"
                           "Examples:\n"
                           "\n"
                           "1. Sentence: I don't know, which to choose.\n"
                           "Output: Oh I think based on what you were looking for the second one would be the best fit."
                           "----------------"
                           "{"
                           "{"
                           "'USER_CONFIRMED_CHOICE': False, "
                           "'LISTING_ID': None "
                           "}"
                           "}"
                           "\n"
                           "\n"
                           "2. Sentence: I love the sound of the third one.\n"
                           "Output: That is a great choice, I will book it right away."
                           "----------------"
                           "{"
                           "{"
                           "'USER_CONFIRMED_CHOICE': True, "
                           "'LISTING_ID': 12677097 "
                           "}"
                           "}"
                           "\n"
                           "\n"
            }

        message_history = [
            system_content,
        ]

    full_result_string = ''
    if results:
        for product in results.docs:
            full_result_string += ' '.join(
                [
                    product.property_type, product.name, f", amenities are:", product.amenities, " Located in city:",
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
            {'role': 'user', 'content': user_input}
        )

    choices = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )['choices']

    answer = choices[0]['message']['content'].strip(" \n")
    message_history.append(
        {'role': choices[0]['message']['role'], 'content': answer}
    )

    return message_history, answer, "'USER_CONFIRMED_CHOICE': True" in answer
