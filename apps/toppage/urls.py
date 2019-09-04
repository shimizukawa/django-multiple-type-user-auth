from django.urls import path
from .views import index, supporter_index, customer_index


app_name = 'toppage'
urlpatterns = [
    path('', index),
    path('supporter/', supporter_index, name='supporter_index'),
    path('customer/', customer_index, name='customer_index'),
]