from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegistrationAndListUserView, LoginAndUserDetailView, LogoutUserView

urlpatterns = [
    path(
        "api/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("user-registration-and-list/", RegistrationAndListUserView.as_view()),
    path("user-login/", LoginAndUserDetailView.as_view()),
    path("user-logout/", LogoutUserView.as_view()),
]
