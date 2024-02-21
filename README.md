# Project Setup
1. Firstly copy the .env file I sent emailed, to the project root folder where manage.py lies, for the database settings.
2. Change memcached to 127.0.0.1 when run locally in the settings file at line 163 otherwise just run "docker compose up".
3. Then run "python3 manage.py runserver || python manage.py runserver" from command line.

## API Description on Postman
1. User-Registration-And-List-API
    a. Post request: {
        "username":"Mando",
        "password":12345,
        "email":"mando@example.com",
        "is_staff":true
    }
    "is_staff" determines if the user is admin user or not. true for admin and false for non-admin
    You will also get an access token, which means that you also have logged in. For all the Booking APIs, In Postman's Authorization section,
    In the bearer token section, Paste the token and then continue with running the API.
    b. Get request: You get a list of all the users created
2. User-Login-API
    a. Post request: {
        "username": "Mando",
        "password": 12345
    }
    You will also get an access and refresh token, which means that you also have logged in. For all the Booking APIs, In Postman's Authorization section,
    In the bearer token section, Paste the access token and then continue with running the API. 
3. User-Logout-API
    a. Post request: {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                             eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNjE5MTI3MywiaWF0IjoxNzA4NDE1MjczLCJqdGkiOiI3ZjU5ZGU3NzEzMjk0MDg0YjMzYjhmYTAyZDBiMGMzNSIsInVzZX  JfaWQiOjF9.41i8XbqQeewQJ6pbOEah3Ds2ZBkZNQi1w9epasyjwik"
        }
    Put the correct refresh token for the logged in user and you will successfully log out.
4. Room-List-And-Create-API: Firstly you should be logged in as an Admin User to use this API.
    a. Post Request: {
        "room_type": "SB" # Only "SB" or "DB" (Single Bed or Double Bed) is allowed, else you get an error.
    }
    b. Get Request: get list of rooms created
5. Create-And-List-Booking_API: Non-Admin users are also allowed
    a. Post Request: {
        "guest_name":"Mando",
        "guest_phone":"9809789675", # Can go 15 characters
        "check_in_date":"2024-01-11",
        "check_out_date":"2024-01-21",
        "guest_address":"millon nagar 12345",
        "room_type":"SB",
        "room_assigned":2
    }

    Date format should be YYYY-MM-DD and check-in-date < check-out-date. Room Asigned should be room_no of an empty unbooked room.
    b. Get Request: Get the list of the bookings by the user.
6. Update-Delete-And-View-Booking-API:
    a. Get Request: As a request param, you should pass an already existing booking id to get the booking detail.
    b. Put Request: Just as 5th point, you can change anything you want. But take care of the dates and room_type
7. Room-Availability-API: Only Admin Users are allowed
    a. Get Request: You should provide query_params
        -> ?check_in_date=2024-01-07&check_out_date=2024-01-12&room_type=SB
        this way. And without providing any of the params, error will be shown.