from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .functions import get_class_data, get_structure_data


def index_view(request):
    """the view function of the index page"""
    context = get_structure_data()
    return render(request=request, template_name='index.html', context=context)


def class_view(request, name=None):
    """the view function of a class page"""
    if name is None:
        return reverse_lazy('index')
    else:
        context = get_class_data(name)
        if not context:
            return reverse_lazy('index')
        return render(request=request, template_name='class.html', context=context)


def framework_view(request, name=None):
    """the view function of a framework page"""
    if name is None:
        return reverse('index')
    else:
        context = get_structure_data(name)
        if not context:
            return reverse('index')
        return render(request=request, template_name='framework.html', context=context)
