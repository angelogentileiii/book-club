from django import template
import re

register = template.Library()


# Custom Tag to Titlecase the input value
@register.filter(name="titlecase")
def titlecase(value):
    if not isinstance(value, str):
        return value

    value = value.lower()

    # Capitalize the first letter of each word after spaces, hyphens, but not after apostrophes
    #   - (?<!'\w) is the negative look behind to check for anything behind the apostrophe which should not be capitalized
    return re.sub(
        r"\b[a-zA-Z](?<!'\w)", lambda match: match.group(0).upper(), value.lower()
    )
