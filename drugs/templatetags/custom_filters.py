from django import template

register = template.Library()

@register.filter
def is_in_group(user, group_names):
    group_list = group_names.split(',')
    return user.groups.filter(name__in=group_list).exists()