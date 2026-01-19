from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),

    path("favorites/<int:event_id>/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("profile/", views.profile, name="profile"),

    path("accounts/signup/", views.signup, name="signup"),
    path("slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
    path("slots/<int:slot_id>/cancel/", views.cancel_slot, name="cancel_slot"),
]
