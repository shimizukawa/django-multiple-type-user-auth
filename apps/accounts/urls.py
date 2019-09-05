from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', include('django.contrib.auth.urls')),
]
