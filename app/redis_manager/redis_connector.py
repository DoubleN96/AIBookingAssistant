import logging

import numpy as np
import redis

from redis.commands.search.field import VectorField
from redis.commands.search.field import TextField
from redis.commands.search.query import Query


def get_redis_connector(host='localhost', port=6379, password=''):
    logging.warning('Connecting to redis...')
    try:
        return redis.Redis(
            host=host,
            port=port,
            password=password
        )
    except Exception as e:
        logging.error(e, exc_info=True)


def get_booking_query(topK):
    logging.warning('Querying redis...')
    return Query(
        f'*=>[KNN {topK} @item_keyword_vector $vec_param AS vector_score]'
    ).sort_by('vector_score').paging(0, topK).return_fields(
        'vector_score', 'property_type', 'name', 'amenities', 'city'
    ).dialect(2)


def create_flat_index(redis_conn, vector_field_name, number_of_vectors, vector_dimensions=512, distance_metric='L2'):
    logging.warning(f'Generating vector index for `{number_of_vectors}` records.')
    redis_conn.ft().create_index([
        VectorField(
            vector_field_name, "FLAT",
            {
                "TYPE": "FLOAT32",
                "DIM": vector_dimensions,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": number_of_vectors,
                "BLOCK_SIZE": number_of_vectors
            }
        ),
        TextField("property_type", as_name='property_type'),
        TextField("name", as_name='name'),
        TextField("amenities", as_name='amenities'),
        TextField("city", as_name='city')
    ])


def load_vectors(client, product_metadata, vector_dict, vector_field_name):
    logging.warning('Loading vectors to redis...')
    p = client.pipeline(transaction=False)
    for index in product_metadata.keys():
        # hash key
        key = 'product_ID: ' + str(product_metadata[index]['listing_id'])

        # hash values
        item_metadata = product_metadata[index]
        item_keywords_vector = vector_dict[index].astype(np.float32).tobytes()
        item_metadata[vector_field_name] = item_keywords_vector

        # HSET
        p.hset(key, mapping=item_metadata)

    p.execute()
