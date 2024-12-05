import random
from django import template
register = template.Library()

@register.simple_tag
def random_key(*values):
    return random.choice(values)