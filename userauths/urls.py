from django.urls import path, include
from userauths import views

urlpatterns = [
    path("sign-up/", views.register_view, name='sign-up'),
    path("sign-in/", views.login_view, name="sign-in"),
    path("logout/", views.logout_view, name="logout"),
]

app_name = "userauths"
