# Choices for movie ratings
# TODO: Add support for non-MPAA rating schemes?
MOVIE_RATINGS = [
    ('G', 'G'),
    ('PG', 'PG'),
    ('PG-13', 'PG-13'),
    ('R', 'R'),
    ('NC-17', 'NC-17'),
    ('X', 'X'),
]

# Mapping fields from TMDB to the media.movies.models.Movie fields
MOVIE_METADATA_FIELD_MAPPING = {
    'title': 'title',
    'alternate_title': 'original_title',
    'release_date': 'release_date',
    'studio': 'production_companies',
    'tagline': 'tagline',
    'summary': 'overview',
    'poster_image': 'poster_path',
    'country': 'production_countries',
}
