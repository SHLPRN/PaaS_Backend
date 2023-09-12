from django.urls import path
from .views import *

urlpatterns = [
    path('get_container_list', get_container_list, name='get_container_list'),
    path('get_container_info', get_container_info, name='get_container_info'),
    path('create_container', create_container, name='create_container'),
    path('start_container', start_container, name='start_container'),
    path('run_container', run_container, name='run_container'),
    path('stop_container', stop_container, name='stop_container'),
    path('remove_container', remove_container, name='remove_container'),
]
