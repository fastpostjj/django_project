from django import template
import datetime

register = template.Library()

# Шаблонный фильтр

@register.filter(name='cut_first')
def cut_text(value):
    return value[:min(len(value), 100)] + '...'


# Шаблонный тэг
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)