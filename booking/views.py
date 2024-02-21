from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from hotel_core.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle


# Create your views here.
class RoomListCreateView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, format=None):
        bookings = Room.objects.all().order_by("-room_no")
        serializer = RoomSerializer(bookings, many=True)
        return Response(
            {
                "data": serializer.data,
                "errors": [],
                "status": "Success",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "data": [],
                "errors": serializer.errors,
                "status": "Failure",
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, format=None):
        bookings = Booking.objects.all().order_by("id")
        serializer = BookingSerializer(bookings, many=True)
        return Response(
            {
                "data": serializer.data,
                "status": "Success",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            room_assigned = serializer.validated_data.get("room_assigned")
            if room_assigned.room_type != serializer.validated_data.get("room_type"):
                return Response(
                    {
                        "data": [],
                        "error": [
                            f"Room number {room_assigned.room_no} is not of room type {serializer.validated_data.get('room_type')}"
                        ],
                        "status": "Failure",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            bookings = room_assigned.bookings.all()

            # Check for overlapping bookings
            for booking in bookings:
                if booking.check_in_date <= serializer.validated_data.get(
                    "check_out_date"
                ) and booking.check_out_date >= serializer.validated_data.get(
                    "check_in_date"
                ):
                    return Response(
                        {
                            "data": [],
                            "errors": [
                                f"This room is booked from {booking.check_in_date} to {booking.check_out_date}"
                            ],
                            "status": "Failure",
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "data": [],
                "errors": serializer.errors,
                "status": "Failure",
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class BookingDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60 * 15))
    def get(self, request, pk, format=None):
        try:
            booking = self.get_object(pk=pk)
            serializer = BookingSerializer(booking)
            return Response(
                {
                    "data": serializer.data,
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {
                    "data": [],
                    "errors": ["Booking not found!"],
                    "status": "Failure",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, pk, format=None):
        try:
            booking = self.get_object(pk=pk)
            serializer = BookingSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "data": serializer.data,
                        "errors": [],
                        "status": "Success",
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response(
                {
                    "data": [],
                    "errors": serializer.errors,
                    "status": "Failure",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        except Http404:
            return Response(
                {
                    "data": [],
                    "errors": ["Booking not found!"],
                    "status": "Failure",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk, format=None):
        try:
            booking = self.get_object(pk=pk)
            booking.delete()
            return Response(
                {
                    "data": ["Booking deleted successfully!"],
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Http404:
            return Response(
                {
                    "data": [],
                    "errors": ["Booking not found!"],
                    "status": "Failure",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class RoomAvailabilityView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, format=None):
        check_in_date = request.query_params.get("check_in_date")
        check_out_date = request.query_params.get("check_out_date")
        room_type = request.query_params.get("room_type")

        if not check_in_date or not check_out_date or not room_type:
            return Response(
                {
                    "data": [],
                    "error": [
                        "Please provide all of start_date, end_date and room_type as query parameters."
                    ],
                    "status": "Failure",
                },
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        try:
            check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {
                    "data": [],
                    "error": [
                        "Invalid date format. Please provide dates in YYYY-MM-DD format."
                    ],
                    "status": "Failure",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if check_out_date < check_in_date:
            return Response(
                {
                    "data": [],
                    "error": [
                        "Invalid dates. You can't go from here if you are not here. We don't allow ghosts to live here."
                    ],
                    "status": "Failure",
                },
                status=status.HTTP_409_CONFLICT,
            )

        if room_type not in Room.ROOM_TYPES:
            return Response(
                {
                    "data": [],
                    "error": [
                        "Invalid room type. Please provide room type from [SB (Single Bed), DB (Double Bed)]."
                    ],
                    "status": "Failure",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if room_type == "SB":
            room_type = Room.SINGLE_BED
        else:
            room_type = Room.DOUBLE_BED

        available_rooms = (
            Room.objects.exclude(
                bookings__check_in_date__lte=check_out_date,
                bookings__check_out_date__gte=check_in_date,
            )
            .filter(
                room_type=room_type,
            )
            .order_by("room_no")
        )

        serializer = RoomSerializer(
            available_rooms,
            many=True,
        )

        return Response(
            {
                "data": serializer.data,
                "errors": [],
                "status": "Success",
            },
            status=status.HTTP_200_OK,
        )
