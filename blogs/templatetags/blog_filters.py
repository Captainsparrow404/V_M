from django import template

register = template.Library()

@register.filter(name='split_tags')
def split_tags(value):
    """
    Split a comma-separated string of tags into a list
    Usage: {{ value|split_tags }}
    """
    if not value:
        return []
    return [tag.strip() for tag in value.split(',') if tag.strip()]