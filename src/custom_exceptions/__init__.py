from src.custom_exceptions.exception_handlers import handle_validation_error
from src.custom_exceptions.exceptions import CustomValidationError

CUSTOM_EXCEPTIONS = [(CustomValidationError, handle_validation_error)]

__all__ = tuple(k for k in locals() if not k.startswith("_"))
