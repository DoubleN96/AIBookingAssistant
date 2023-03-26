import logging

import pandas as pd


def get_room_dataframe(source_file='/home/chatbot_fastapi/app/data/airbnb.csv'):
    logging.info(f'Loading source file: `{source_file}`.')
    room_data = pd.read_csv(
        source_file, delimiter=',', encoding_errors='ignore', on_bad_lines='skip', low_memory=False
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
            'listing_id', 'name', 'host_id', 'host_since', 'host_location',
            'host_is_superhost', 'host_total_listings_count',
            'host_has_profile_pic', 'host_identity_verified', 'neighbourhood',
            'district', 'city', 'city_id', 'property_type',
            'room_type', 'accommodates', 'bedrooms', 'amenities', 'price',
            'minimum_nights', 'maximum_nights', 'review_scores_rating',
            'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value', 'instant_bookable'
        ]
    ], city_mapping

