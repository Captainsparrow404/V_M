from django import template
import re

register = template.Library()


@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed URL"""
    if not url:
        return ''

    # Handle youtube.com URLs
    youtube_regex = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'

    # Handle youtu.be URLs
    youtu_be_regex = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)'
    match = re.search(youtu_be_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'

    return url


@register.filter
def vimeo_embed(url):
    """Convert Vimeo URL to embed URL"""
    if not url:
        return ''

    vimeo_regex = r'(?:https?://)?(?:www\.)?vimeo\.com/(\d+)'
    match = re.search(vimeo_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://player.vimeo.com/video/{video_id}'

    return url


@register.filter
def split_tags(tags_string):
    """Split comma-separated tags into a list"""
    if not tags_string:
        return []
    return [tag.strip() for tag in tags_string.split(',') if tag.strip()]
