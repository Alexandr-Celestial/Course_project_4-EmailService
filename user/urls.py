from django.urls import path

from user.apps import UserConfig
from user.views import login_user, logout_user, CreateUserView, validation_user, UserListView, block_user

app_name = UserConfig.name

urlpatterns = [
    path("", login_user, name="auth"),
    path("logout/", logout_user, name="logout"),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('valid_token/<str:token>', validation_user, name='valid_token'),
    path('block_user/<int:pk>/', block_user, name='block_user'),
    path('users_services/', UserListView.as_view(), name='users_services'),
]
