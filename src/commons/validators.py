from typing import Optional

from commons.errors import Error


class ValidationException(Exception):
    __slots__ = ('parameters', 'code')

    def __init__(self, parameters: Optional[dict] = None, code: str = None):
        self.parameters = parameters
        self.code = f"VALIDATION.{code}" if code else "VALIDATION.ERROR"

    @classmethod
    def single(cls, field, error):
        return cls(parameters={field: error})

    @classmethod
    def general(cls, error: Error):
        return cls(code=error.code, parameters=error.parameters)
