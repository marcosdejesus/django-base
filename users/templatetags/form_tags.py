from django import template

register = template.Library()

def field_type(field):
    """Return the type of a field"""
    return field.field.widget.__class__.__name__

@register.filter
def field_css_class(field):
    """ Return the proper CSS class for a field"""
    css_class = ''
    if field.form.is_bound:
        if field.errors:
            css_class = 'is_invalid'
        elif field_type(field) != 'PasswordInput':
            css_class = 'is_valid'
    return 'form-control {}'.format(css_class)
