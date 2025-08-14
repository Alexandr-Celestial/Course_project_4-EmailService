from django import template

register = template.Library()


@register.filter()
def spl_fn(fullname):
    first_name, *last_name = str(fullname).split(" ")
    return f"{first_name[0].upper()}"
