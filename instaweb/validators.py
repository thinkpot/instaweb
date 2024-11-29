# validators.py
import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    # Define a regex pattern for valid phone numbers (10 digits for simplicity)
    pattern = r'^\+?1?\d{9,15}$'

    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid phone number. It must be between 10 and 15 digits."
        )
