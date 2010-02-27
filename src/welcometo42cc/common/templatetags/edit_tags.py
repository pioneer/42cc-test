from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_user(user):
    return reverse('admin:auth_user_change', args=(user.id,))
