import logging

import pandas as pd


def get_room_dataframe(source_file='/home/chatbot_fastapi/app/data/tripath.csv'):
    logging.info(f'Loading source file: `{source_file}`.')
    room_data = pd.read_csv(
        source_file, delimiter='\t', encoding_errors='ignore', on_bad_lines='skip', low_memory=False
    )
    room_data['city_id'] = room_data.city.astype('category').cat.codes
    room_data = room_data.groupby(
        'city', group_keys=False
    ).apply(lambda x: x.sample(min(len(x), 2000))).reset_index(drop=True)
    city_mapping = {
        city_item[0][0]: city_item[0][1] for city_item in room_data[['city', 'city_id']].value_counts().items()
    }
    return room_data[
        [
            'listing_id', 'description', 'city', 'city_id', 'status', 'CHECK-IN', 'CHECK-OUT', 'price'
        ]
    ], city_mapping

