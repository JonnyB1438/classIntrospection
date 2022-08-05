from django.urls import path

from .views import index_view, framework_view, class_view

urlpatterns = [
    path('', index_view, name='index'),
    path('class/<str:name>', class_view, name='class'),
    path('framework/<str:name>', framework_view, name='framework'),
]
