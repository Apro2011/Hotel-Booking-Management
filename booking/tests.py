from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Room, Booking
from django.urls import reverse


class BaseTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nonadmin",
            password="12345",
            email="nonadmin@example.com",
            is_staff=False,
        )
        self.client.force_authenticate(user=self.user)


class TestRoomListCreateView(BaseTestCase):
    def test_create_room(self):
        self.room_data = {
            "room_type": Room.SINGLE_BED,
        }
        url = reverse("room_list_and_create")
        response = self.client.post(url, data=self.room_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_room(self):
        url = reverse("room_list_and_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBookingListCreateView(BaseTestCase):
    def test_create_booking_no_overlapping_dates(self):
        self.room = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        self.booking_data = {
            "guest_name": "John Wilson",
            "guest_phone": "8907896781",
            "guest_address": "Mgar Nagar, Bangalore 12678",
            "check_in_date": "2024-01-12",
            "check_out_date": "2024-01-20",
            "room_type": Booking.SINGLE_BED,
            "room_assigned": self.room.room_no,
        }
        url = reverse("create_and_list_booking")
        response = self.client.post(url, data=self.booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_booking_overlapping_dates(self):
        self.room = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        Booking.objects.create(
            guest_name="Black Wes",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.SINGLE_BED,
            room_assigned=self.room,
        )
        self.booking_data = {
            "guest_name": "John Wilson",
            "guest_phone": "8907896781",
            "guest_address": "Mgar Nagar, Bangalore 12678",
            "check_in_date": "2024-01-10",
            "check_out_date": "2024-01-20",
            "room_type": Booking.SINGLE_BED,
            "room_assigned": self.room.room_no,
        }
        url = reverse("create_and_list_booking")
        response = self.client.post(url, data=self.booking_data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_list_bookings(self):
        url = reverse("create_and_list_booking")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBookingDetailUpdateView(BaseTestCase):
    def test_update_booking(self):
        self.room = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        booking = Booking.objects.create(
            guest_name="Black Wes",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.SINGLE_BED,
            room_assigned=self.room,
        )
        self.booking_updated_data = {
            "guest_phone": "8978675645",
            "check_out_date": "2024-01-17",
        }
        url = reverse("update_delete_and_view_booking", kwargs={"pk": booking.pk})
        response = self.client.put(url, data=self.booking_updated_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_booking_details(self):
        self.room = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        booking = Booking.objects.create(
            guest_name="Black Wes",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.SINGLE_BED,
            room_assigned=self.room,
        )
        url = reverse("update_delete_and_view_booking", kwargs={"pk": booking.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_booking(self):
        self.room = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        booking = Booking.objects.create(
            guest_name="Black Wes",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.SINGLE_BED,
            room_assigned=self.room,
        )
        url = reverse("update_delete_and_view_booking", kwargs={"pk": booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestRoomAvailabilityView(BaseTestCase):
    def test_check_room_availability(self):
        self.room1 = Room.objects.create(
            room_type=Room.SINGLE_BED,
        )
        Booking.objects.create(
            guest_name="Black Wes",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.SINGLE_BED,
            room_assigned=self.room1,
        )
        self.room2 = Room.objects.create(
            room_type=Room.DOUBLE_BED,
        )
        Booking.objects.create(
            guest_name="Black Ols",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.DOUBLE_BED,
            room_assigned=self.room2,
        )
        self.room3 = Room.objects.create(
            room_type=Room.DOUBLE_BED,
        )
        Booking.objects.create(
            guest_name="Black Ponsw",
            guest_phone="9089786756",
            guest_address="Mgar Nagar, Bangalore 12678",
            check_in_date="2024-01-12",
            check_out_date="2024-01-20",
            room_type=Booking.DOUBLE_BED,
            room_assigned=self.room3,
        )
        rooms_list = [Room(room_type="SB") for _ in range(10)]
        for _ in range(10):
            rooms_list.append(Room(room_type="DB"))
        self.rooms_bulk = Room.objects.bulk_create(rooms_list)

        # Non Admin User Error Test
        url = f"{reverse('room_availability')}?check_in_date=2024-01-12&check_out_date=2024-01-21&room_type=DB"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User Success Test
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin",
            password="12345",
            email="admin@example.com",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Missing check_out_date
        url = f"{reverse('room_availability')}?check_in_date=2024-01-12&room_type=DB"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_417_EXPECTATION_FAILED)

        # Missing room_type
        url = f"{reverse('room_availability')}?check_in_date=2024-01-12&check_out_date=2024-01-21"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_417_EXPECTATION_FAILED)

        # Check Out Date < Check In Date
        url = f"{reverse('room_availability')}?check_in_date=2024-01-21&check_out_date=2024-01-12&room_type=DB"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # Room Type other than "SB" and "DB" Error
        url = f"{reverse('room_availability')}?check_in_date=2024-01-12&check_out_date=2024-01-21&room_type=LL"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        # Invalid date format error
        url = f"{reverse('room_availability')}?check_in_date=20-01-2024&check_out_date=2024-01-12&room_type=DB"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
