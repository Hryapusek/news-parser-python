
class ErrorResponseCodeException(Exception):
    def __init__(self, *args) -> None:
        Exception.__init__(self, args)
