import os

from media.constants import VALID_VIDEO_EXTENSIONS

IGNORED_TITLE_WORDS = ['a', 'an', 'the']


def generate_sort_title(title):
    title_words = title.split(' ')
    if title_words[0].lower() in IGNORED_TITLE_WORDS:
        removed_word = title_words[0]
        title_words.pop(0)
        return ' '.join(title_words) + f', {removed_word}'
    else:
        return title


def get_title_year_from_filepath(filepath):
    """
    Extracts the title and year (if present) from a properly formatted filepath string.
    """
    parts = os.path.splitext(filepath)[0].split('/')
    try:
        title, year = parts[-1].split('(')
    except ValueError:
        return parts[-1], None
    return ' '.join(title.split(' ')[:-1]), year.replace(')', '') if year else None


def validate_filepath(filepath):
    """
    Validates the filepath by checking if the file extension is a supported type.
    """
    return os.path.splitext(filepath)[-1] in VALID_VIDEO_EXTENSIONS
