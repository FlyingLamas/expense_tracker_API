from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import registration_view, logout_view
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    # Following url patterns are used for Token authentication
    # path("login/", obtain_auth_token, name = "login"),
    path("register/", registration_view, name = "register"),
    path("logout/", logout_view, name = "logout"),
    
    # Following url patterns are used for JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


