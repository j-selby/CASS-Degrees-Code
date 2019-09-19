"""
Template tags specific to the student facing frontend. These generate interactive sections
for courses to be added.
"""

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
