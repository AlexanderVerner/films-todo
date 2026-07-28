from urllib.parse import urlparse
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def _format_person(person):
    if isinstance(person, str):
        return person
    if isinstance(person, dict):
        parts = []
        for name_ru, name_en in person.items():
            if name_ru and name_en and name_ru != name_en:
                parts.append(f'{name_ru} / {name_en}')
            elif name_ru:
                parts.append(name_ru)
            elif name_en:
                parts.append(name_en)
        return ', '.join(parts)
    return ''


@register.filter
def format_person_list(people):
    if not people:
        return ''
    formatted = [_format_person(person) for person in people]
    return ', '.join(item for item in formatted if item)


def _is_safe_url(url):
    """Validate URL scheme to prevent XSS attacks."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()
        return scheme in ('http', 'https')
    except Exception:
        return False


@register.filter
def format_watchability(sources):
    if not sources:
        return ''
    links = []
    for item in sources:
        if not isinstance(item, dict):
            continue
        url = item.get('url')
        if not url:
            continue
        name = item.get('name') or item.get('platform') or url
        
        # Validate URL scheme to prevent XSS
        if _is_safe_url(url):
            links.append(
                f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
                f'{escape(name)}</a>'
            )
        else:
            # For unsafe URLs, output platform name only
            links.append(escape(name))
    
    return mark_safe(', '.join(links))


@register.filter
def format_rating(value):
    if value is None or value == '':
        return ''
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    formatted = f'{number:.1f}'
    if formatted.endswith('.0'):
        return formatted[:-2]
    return formatted
