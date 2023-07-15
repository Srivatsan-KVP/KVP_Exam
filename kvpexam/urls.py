from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seating/', include('seating.urls')),
    path('/', include('app.urls')),
]
