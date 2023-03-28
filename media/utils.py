IGNORED_TITLE_WORDS = ['a', 'an', 'the']


def generate_sort_title(title):
    title_words = title.split(' ')
    if title_words[0].lower() in IGNORED_TITLE_WORDS:
        removed_word = title_words[0]
        title_words.pop(0)
        return ' '.join(title_words) + f', {removed_word}'
    else:
        return title
