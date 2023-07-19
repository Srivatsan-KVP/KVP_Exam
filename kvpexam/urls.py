from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('admin/', include('admin.urls')),
    path('', include('app.urls')),
]
