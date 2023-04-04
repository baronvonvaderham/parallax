class InvalidFilepathError(Exception):

    def __init__(self, filepath):
        self.message = f'Invalid filepath supplied, unable to process: {filepath}'
        super().__init__(self.message)


class DuplicateMediaError(Exception):

    def __init__(self, filepath, media_type):
        self.message = f'{media_type} already exists for file provided: {filepath}'
        super().__init__(self.message)


class MediaNotFoundError(Exception):

    def __init__(self, filepath, media_type):
        self.message = f'{media_type} not found for filepath provided: {filepath}'
