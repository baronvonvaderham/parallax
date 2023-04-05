TV_AUDIENCE_LABEL = [
    ('Y', 'Y'),
    ('Y7', 'Y7'),
    ('G', 'G'),
    ('PG', 'PG'),
    ('14', '14'),
    ('MA', 'MA'),
]
TV_CONTENT_LABEL = [
    ('D', 'D'),
    ('L', 'L'),
    ('S', 'S'),
    ('V', 'V'),
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('GL', 'GL'),
    ('MV', 'MV'),
    ('GV', 'GV'),
    ('BN', 'BN'),
    ('N', 'N'),
    ('SSC', 'SSC'),
    ('RP', 'RP'),
]

TV_METADATA_FIELD_MAPPING = {
    'title': 'name',
    'alternate_title': 'original_name',
    'premiere_date': 'first_air_date',
    'network': 'networks',
    'summary': 'overview',
    'poster_image': 'poster_path',
    'country': 'origin_country',
}

SEASON_METADATA_FIELD_MAPPING = {
    'number': 'season_number',
    'start_data': 'air_date',
    'summary': 'overview',
    'poster_image': 'poster_path',
}
