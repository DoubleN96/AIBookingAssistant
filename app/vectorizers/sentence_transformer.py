import logging
import pandas as pd

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    'sentence-transformers/all-distilroberta-v1', cache_folder='/home/chatbot_fastapi/', device='cuda:0'
)

MAX_TEXT_LENGTH = 400


def auto_truncate(val):
    return str(val)[:MAX_TEXT_LENGTH]


def get_data_vectors(room_data: pd.DataFrame):
    logging.warning(f'Vectorizing index data...')
    # get the first 1000 products with non-empty item keywords
    rooms_metadata = room_data.to_dict(orient='index')
    item_keywords = [
        ', '.join(auto_truncate(rooms_metadata[i][key]) for key in [
            'city', 'description', 'price'
            ]
        )
        for i in rooms_metadata.keys()
    ]
    return [model.encode(sentence) for sentence in item_keywords]
