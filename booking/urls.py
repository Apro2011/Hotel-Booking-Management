from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    BookingListCreateView,
    BookingDetailUpdateView,
    RoomListCreateView,
    RoomAvailabilityView,
)


urlpatterns = [
    path("room-list-and-create/", RoomListCreateView.as_view()),
    path("create-and-list-booking/", BookingListCreateView.as_view()),
    path("update-delete-and-view-booking/<int:pk>/", BookingDetailUpdateView.as_view()),
    path("room-availability/", RoomAvailabilityView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
