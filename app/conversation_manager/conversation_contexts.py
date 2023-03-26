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
        redis_connector,
        city_code
):
    interaction_count += + 1
    logging.warning(interaction_count)
    if interaction_count == 1:
        # Run the chain only specifying the input variable.
        keywords = booking_chain.run(
            user_input + ', in city: ' + context_entities['CITY'] + ', these are reservation specification: ' + str(context_entities)
        )
        logging.warning(
            user_input + ', in city: ' + context_entities['CITY'] + ', these are reservation specification: ' + str(context_entities)
        )
        logging.warning(keywords)
        logging.warning(city_code)

        top_k = 3
        # vectorize the query
        query_vector = vectorizer.encode(keywords).astype(np.float32).tobytes()
        params_dict = {"vec_param": query_vector}

        # Execute the query
        results = redis_connector.ft().search(
            get_booking_query(top_k, city_code=city_code), query_params=params_dict
        )
        logging.warning(results)
    else:
        results = {}
    if results:
        user_ask = user_input + ', specification of booking requirements: ' + str(context_entities)
    else:
        user_ask = user_input

    message_history, answer, = recommend_found_bookings(
        message_history,
        results, user_ask
    )
    return message_history, answer, interaction_count


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
                "content": "You are a REST API SYSTEM connected to AI booking asistant,"
                           "when given three booking options, you give description, you provide JSON OUTPUT,"
                           "Output:\n"
                           "{"
                           "'ANSWER': 'Nice description of the three options'"
                           "'USER_CONFIRMED_CHOICE': Boolean True or False value "
                           "based on whether positive confirmation was given by user, "
                           "'LISTING_ID': LISTING_ID which is the id of the apartment "
                           "if USER_CONFIRMED_CHOICE is True, "
                           "}\n"
                           "You are connected to nice AI booking ASSISTANT. "
                           "AI booking ASSISTANT is NEVER FORGETS TO PRESENT each of three previously given options, "
                           "and tries to sell and tell a little bit about each of three offers,"
                           "REST API SYSTEM has consistent output.\n"
                           "After presenting the options, "
                           "REST API SYSTEM OUTPUTS JSON containing an ANSWER from AI booking ASSISTANT and "
                           "information of state of confirmation and "
                           "booking id in USER_CONFIRMED_CHOICE and LISTING_ID.\n"
                           "After confirmation is received you might also "
                           "ask if user needs recommendations for things to do in the city."
                           "YOU DONT ASK QUESTIONS ABOUT THE BOOKING, YOU DO NOT ASK FOR ADDITIONAL INFORMATION, "
                           "YOU only ask for choice confirmation at the begging and "
                           "YOU ALWAYS GIVE OUTPUT as JSON, see example bellow."
                           "YOU ARE A REST API, YOUR OUTPUT FORMAT IS JSON"
                           "\n\n"
                           "OUTPUT Format definition:"
                           "{"
                           "'ANSWER': 'Nice description of the three options',"
                           "'USER_CONFIRMED_CHOICE': Boolean True or False value "
                           "based on whether positive confirmation was given by user, "
                           "'LISTING_ID': LISTING_ID which is the id of the apartment "
                           "if USER_CONFIRMED_CHOICE is True,"
                           "}\n\n"
                           "Examples:\n"
                           "1. Sentence: I don't know, which to choose.\n"
                           "Output:"
                           "{"
                           "'ANSWER': 'Oh I think based on what you were looking for, "
                           "the second one would be the best fit.',"
                           "'USER_CONFIRMED_CHOICE': False, "
                           "'LISTING_ID': None "
                           "}"
                           "\n"
                           "\n"
                           "2. Sentence: I love the sound of the third one.\n"
                           "Output:"
                           "{"
                           "'ANSWER': 'That is a great choice, I will record to booking for you right away.', "
                           "'USER_CONFIRMED_CHOICE': True, "
                           "'LISTING_ID': 12677097 "
                           "}"
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


def get_location_recommendations_response(message_history: list[dict], user_input: str):
    if not message_history:
        message_history = [
            {
                "role": "system",
                "content": "You are the booking assistant answering touristy questions about "
                           "the city user booked his booking at."
            },
            {"role": "user", "content": user_input}
        ]
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature=0.4
    )

