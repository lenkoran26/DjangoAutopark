from django.urls import path
from .views import register, register_done, LoginUser, LogoutUser, ProfileView, index


app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name="register"),
    path('register-done/', register_done, name="register_done"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogoutUser.as_view(), name="logout"),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),

]