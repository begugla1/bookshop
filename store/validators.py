from django.core.exceptions import ValidationError


def discount_validator(value):
    if value > 1 or value < 0:
        raise ValidationError('Discount is invalid!')
    return value
