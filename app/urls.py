from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/', views.profile),

    path('', views.main),
    path('admin/', views.admin),

    path('saved/<str:date>/', views.saved)   
]
