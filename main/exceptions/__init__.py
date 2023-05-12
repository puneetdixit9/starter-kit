from main.exceptions.errors import (
    CustomValidationError,
    RecordNotFoundError,
    UnauthorizedUserError,
)
from main.exceptions.handlers import (
    handle_record_not_found_error,
    handle_unauthorized_user_error,
    handle_validation_error,
)

# A list of custom exceptions and their handlers, This list is used to register custom errors with
# flask app.
CUSTOM_EXCEPTIONS = [
    (CustomValidationError, handle_validation_error),
    (UnauthorizedUserError, handle_unauthorized_user_error),
    (RecordNotFoundError, handle_record_not_found_error),
]
