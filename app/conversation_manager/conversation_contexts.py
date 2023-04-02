# gtp4 based interpretation
import logging
import numpy as np
import openai
from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query


def append_message_history(message_history, role, content):
    message_history.append(
        {"role": role, "content": content.strip(" \n")}
    )


def create_choices(messages, temperature=0.4):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )['choices']


def recommend_booking(
        message_history,
        user_input: str,
        interaction_count: int,
        booking_chain,
        context_entities: dict,
        redis_connector,
        city_code
):
    interaction_count += 1
    logging.warning(interaction_count)
    if interaction_count == 1:
        message_history = []
        user_input_formatted = f"{user_input}, in city: {context_entities['CITY']}, these are reservation specification: {context_entities}"
        keywords = booking_chain.run(user_input_formatted)
        logging.warning(user_input_formatted)
        logging.warning(keywords)
        logging.warning(city_code)

        top_k = 3
        query_vector = vectorizer.encode(keywords).astype(np.float32).tobytes()
        params_dict = {"vec_param": query_vector}

        results = redis_connector.ft().search(
            get_booking_query(top_k, city_code=city_code), query_params=params_dict
        )
        logging.warning(results)
    else:
        results = {}
    if results:
        user_ask = f"{user_input}, specification of booking requirements: {context_entities}"
    else:
        user_ask = user_input

    message_history, answer = recommend_found_bookings(message_history, results, user_ask)
    return message_history, answer, interaction_count


def ask_for_booking_details(message_history: list[dict], user_input: str, booking_known_info: dict):
    known = list(booking_known_info.keys()) if booking_known_info else []

    if not message_history:
        needed_entities = [ent_name for ent_name in ['FULL_NAME', 'DATES', 'CITY', 'BUDGET', 'GUEST_COUNT'] if ent_name not in known]

        system_content = {
            "role": "system",
            "content": "User is asking to book a room and you are "
                       "generic company room or apartment booking ASSISTANT "
                       "asking USER for information to make the booking,"
        }

        system_content['content'] += (
            f"ONLY ask him nicely for these information on `{', '.join(needed_entities)}`for his booking."
            f"You ask ONLY about: `{', '.join(needed_entities)}`"
        )
        message_history = [
            system_content,
            {"role": "user", "content": user_input}
        ]
    else:
        append_message_history(message_history, "user", user_input)

    choices = create_choices(message_history)
    answer = choices[0]['message']['content'].strip(" \n")
    append_message_history(message_history, choices[0]['message']['role'], answer)

    return answer, message_history


def recommend_found_bookings(message_history, results, user_input):
    if not message_history:
        system_content = {
            ...
        }
        message_history = [system_content]

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
        append_message_history(message_history, "user", f'My accomodation booking options are: {full_result_string}')
    else:
        append_message_history(message_history, "user", user_input)

    choices = create_choices(message_history, temperature=0.3)
    answer = choices[0]['message']['content'].strip(" \n")
    append_message_history(message_history, choices[0]['message']['role'], answer)

    return message_history, answer


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
        append_message_history(message_history, "user", user_input)

    choices = create_choices(message_history, temperature=0.4)
    answer = choices[0]['message']['content'].strip(" \n")
    append_message_history(message_history, choices[0]['message']['role'], answer)

    return message_history, answer


def get_location_recommendations_response(message_history: list[dict], user_input: str):
    if not message_history:
        system_content = {
            ...
        }
        message_history = [system_content]
    append_message_history(message_history, "user", user_input)

    choices = create_choices(message_history, temperature=0.4)
    answer = choices[0]['message']['content'].strip(" \n")
    append_message_history(message_history, choices[0]['message']['role'], answer)

    return message_history, answer
