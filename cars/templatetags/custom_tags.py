from django import template

register = template.Library()

@register.filter
def format_tenge(value):
    try:
        value = float(value)
        parts = f"{value:,.2f}".split(".")
        integer_part = parts[0].replace(",", " ")
        return f"{integer_part}.{parts[1]}"
    except:
        return value