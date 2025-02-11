from django import template
import re

register = template.Library()


@register.filter(name="titlecase")
def titlecase(value):
    """Capitalizes the first letter of each word, even after hyphens and spaces."""
    return re.sub(r"\b[a-zA-Z]", lambda match: match.group(0).upper(), value)
