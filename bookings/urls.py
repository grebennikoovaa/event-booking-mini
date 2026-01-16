from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                 # главная (редирект)
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
    path("slots/<int:slot_id>/cancel/", views.cancel_slot, name="cancel_slot"),
]
