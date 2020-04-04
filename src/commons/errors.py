from dataclasses import dataclass
from typing import Optional


@dataclass
class Error:
    __slots__ = ('code', 'parameters')
    code: str
    parameters: Optional[dict]

    @classmethod
    def new(cls, code: str):
        return cls(code, None)

    def to_dict(self):
        return {"code": self.code} if not self.parameters else {"code": self.code, "parameters": self.parameters}


invalid_object = Error("INVALID_KIND", {"expected": "object"})
invalid_string = Error("INVALID_KIND", {"expected": "string"})
invalid_uuid = Error("INVALID_KIND", {"expected": "UUID"})
invalid_bool = Error("INVALID_KIND", {"expected": "bool"})
invalid_number = Error("INVALID_KIND", {"expected": "number"})

error_missing = Error.new("MISSING")


def too_small(min):
    return Error("TOO_SMALL", {"required": min})


def too_big(max):
    return Error("TOO_BIG", {"required": max})
