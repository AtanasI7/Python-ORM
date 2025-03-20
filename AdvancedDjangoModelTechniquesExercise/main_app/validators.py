import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value: str):
        for c in value:
            if not (c.isalpha() or c.isspace()):
                raise ValidationError(self.message)


@deconstructible
class PhoneNumberValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value: str):
        if not re.match(r'^\+\350\d{9}$', value):
            raise ValidationError(self.message)

