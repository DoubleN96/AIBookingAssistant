import logging

import numpy as np

import openai


from app.vectorizers.sentence_transformer import model as vectorizer
from app.redis_manager.redis_connector import get_booking_query
from recommend_found_bookings import recommend_found_bookings

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
        message_history = []
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
