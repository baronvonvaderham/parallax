class InvalidFilepathError(Exception):

    def __init__(self, filepath):
        self.message = f'Invalid filepath supplied, unable to process: {filepath}'
        super().__init__(self.message)
