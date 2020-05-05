from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

def random_filter(value, is_safe = True):
    print('filter')
    result = re.sub(r'(?<=\[)?(?P<link>\w+)\]?', r'\g<link>' , value)
    res = re.findall(r'\[(?P<link>\w+)\]?', value)
    if res != []:
        response = value
        for r in res:
            sub = "<a href =%s?word=%s>%s</a>" % ('/', res[0], res[0])
            response = re.sub(f'\[{res[0]}\]', sub, response)
    else:
        response = value
    return mark_safe(response)

register.filter('random_filter', random_filter)