from src.custom_exceptions.exceptions import CustomValidationError
from src.custom_exceptions.exception_handlers import handle_validation_error

CUSTOM_EXCEPTIONS = [
    (CustomValidationError, handle_validation_error)
]
