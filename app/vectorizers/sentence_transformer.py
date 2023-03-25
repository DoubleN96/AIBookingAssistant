import logging
import pandas as pd

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    'sentence-transformers/all-distilroberta-v1', cache_folder='/home/chatbot_fastapi/app/data/', device='cuda:0'
)

MAX_TEXT_LENGTH = 400
NUMBER_PRODUCTS = 10000


def auto_truncate(val):
    return str(val)[:MAX_TEXT_LENGTH]


def get_data_vectors(room_data: pd.DataFrame):
    logging.warning(f'Vectorizing index data...')

    # get the first 1000 products with non-empty item keywords
    rooms_metadata = room_data.head(NUMBER_PRODUCTS).to_dict(orient='index')
    item_keywords = [
        ', '.join(auto_truncate(rooms_metadata[i][key]) for key in [
            'name', 'host_location', 'neighbourhood', 'property_type', 'amenities', 'price'
            ]
        )
        for i in rooms_metadata.keys()
    ]
    return [model.encode(sentence) for sentence in item_keywords]
