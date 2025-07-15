from django import template
import re

register = template.Library()

@register.filter
def youtube_video_id(url):
    if not url:
        return ''
    
    # Extract video ID from various YouTube URL formats
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    match = re.search(youtube_regex, url)
    if match:
        return match.group(6)
    return '' 