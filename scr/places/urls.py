from django.urls import path
from .views import *

app_name = 'places'

urlpatterns = [
    path('add_place/', add_place, name='add_place'),
    path('', places, name="places"),
    path('<slug:slug>', place_detail, name='place_detail'),
    path('delete/<slug:slug>/', place_delete, name='delete_place'),
]
