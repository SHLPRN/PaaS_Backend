from django.urls import path
from .views import *

urlpatterns = [
    path('list_nodes', list_nodes, name='list_nodes'),
    path('list_pods', list_pods, name='list_pods'),
    path('list_deployments', list_deployments, name='list_deployments'),
    path('create_deployment', create_deployment, name='create_deployment'),
    path('update_deployment', update_deployment, name='update_deployment'),
    path('delete_deployment', delete_deployment, name='delete_deployment'),
    path('list_services', list_services, name='list_services'),
    path('create_service', create_service, name='create_service'),
    path('update_service', update_service, name='update_service'),
    path('delete_service', delete_service, name='delete_service'),
    path('get_host_params', get_host_params, name='get_host_params'),
]
