from django.urls import path
from .views import *

urlpatterns = [
    path('list_images', list_images),
    path('remove_image', remove_image),
    path('pull_image', pull_image),
    path('build_image', build_image),
]
