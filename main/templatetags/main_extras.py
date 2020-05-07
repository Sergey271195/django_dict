from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

def link_filter(value, is_safe = True):
    result = re.sub(r'(?<=\[)?(?P<link>\w+)\]?', r'\g<link>' , value)
    res = re.findall(r'\[{1}(?P<link>(\w+\s?)*)\]{1}', value)
    res = [r[0] for r in res]
    if res != []:
        response = value
        for r in res:
            sub = "<a href =%s?word=%s><em>%s</em></a>" % ('/', r, r)
            response = re.sub(f'\[{r}\]', sub, response)
    else:
        response = value
    return mark_safe(response)

def style_filter(value, is_safe = True):
    value = re.sub(r'{bc}', '<b>: </b>', value)
    value = re.sub(r'{ldquo}', '&ldquo;', value)
    value = re.sub(r'{rdquo}', '&rdquo;', value)
    value = re.sub(r'{dx}', '<br/>&#8212; ', value)
    value = re.sub(r'{/dx}', '', value)
    value = re.sub(r'{dx_def}', '(', value)
    value = re.sub(r'{/dx_def}', ')', value)
    value = re.sub(r'{it}', '<em>', value)
    value = re.sub(r'{wi}', '<em>', value)
    value = re.sub(r'{/it}', '</em>', value)
    value = re.sub(r'{/wi}', '</em>', value)
    value = re.sub(r'{ma}', '&#8212; more at  ', value)
    value = re.sub(r'{/ma}', '', value)
    return mark_safe(value)

register.filter('link_filter', link_filter)
register.filter('style_filter', style_filter)