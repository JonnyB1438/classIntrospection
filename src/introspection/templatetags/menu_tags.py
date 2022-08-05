from django import template
from ..settings import menu_dict

register = template.Library()


@register.simple_tag()
def get_frameworks():
    return [framework for framework in menu_dict]


@register.simple_tag()
def get_framework(name):
    return menu_dict[name]


@register.simple_tag()
def get_module(class_name):
    for framework in menu_dict.values():
        for module_name, module in framework.items():
            if class_name in module:
                return {'name': module_name, 'classes': module}
    return {}
