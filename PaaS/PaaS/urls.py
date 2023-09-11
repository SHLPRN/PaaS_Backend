from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/application/', include('application.urls')),
    path('api/container/', include('container.urls')),
    path('api/image/', include('image.urls')),
]
