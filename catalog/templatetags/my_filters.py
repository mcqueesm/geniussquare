from django import template
register = template.Library()

@register.filter(name='temprange') 
def temprange(n):
    return range(n)