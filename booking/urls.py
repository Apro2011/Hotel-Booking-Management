from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    BookingListCreateView,
    BookingDetailUpdateView,
    RoomListCreateView,
    RoomAvailabilityView,
)


urlpatterns = [
    path(
        "room-list-and-create/",
        RoomListCreateView.as_view(),
        name="room_list_and_create",
    ),
    path(
        "create-and-list-booking/",
        BookingListCreateView.as_view(),
        name="create_and_list_booking",
    ),
    path(
        "update-delete-and-view-booking/<int:pk>/",
        BookingDetailUpdateView.as_view(),
        name="update_delete_and_view_booking",
    ),
    path(
        "room-availability/", RoomAvailabilityView.as_view(), name="room_availability"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
