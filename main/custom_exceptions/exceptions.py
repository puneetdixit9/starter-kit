class CustomValidationError(Exception):
    """
    This is the custom exception class for validation error. Raise this exception when request
    have invalid data.
    """

    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400


class UnauthorizedUserError(Exception):
    """
    This is the custom exception class to raise unauthorized user error
    """

    def __init__(self):
        super().__init__("Unauthorized user")
        self.status_code = 401


class RecordNotFoundError(Exception):
    """
    This is the custom exception class to raise an error is record not found.
    """

    def __init__(self):
        super().__init__("Record not found!!!")
        self.status_code = 404
