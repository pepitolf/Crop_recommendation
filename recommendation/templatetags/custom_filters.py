from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    if hasattr(value, 'field') and hasattr(value.field, 'widget'):
        existing_classes = value.field.widget.attrs.get('class', '')
        new_classes = f'{existing_classes} {css_class}'.strip()
        return value.as_widget(attrs={'class': new_classes})
    return value

@register.filter(name='add_placeholder')
def add_placeholder(value, placeholder):
    if hasattr(value, 'field') and hasattr(value.field, 'widget'):
        return value.as_widget(attrs={'placeholder': placeholder})
    return value
