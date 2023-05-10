from django import template
import datetime

register = template.Library()

# Шаблонный фильтр
@register.filter
def first_text(value):
    return value[:100]

@register.filter(name='reverse')
def reverse_text(value):
    return value[:min(len(value), 100)]


# Шаблонный тэг
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)