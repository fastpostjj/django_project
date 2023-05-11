from django import template


register = template.Library()

# Шаблонный фильтр

@register.filter(name='cut_first')
def cut_text(value):
    return value[:min(len(value), 100)] + '...'


# Шаблонный тэг
@register.simple_tag
def get_data(obj):
    return f"{obj.name} Цена: {obj.price} {obj.category}"

