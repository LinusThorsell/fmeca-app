from django.urls import path
from . import views

urlpatterns = [
    path('person-list/', views.PersonList, name="person-list"),
]
