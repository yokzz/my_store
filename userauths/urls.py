from django.urls import path, include
from userauths import views

urlpatterns = [
    path("signup/", views.register_view, name='sign-up'),
    path("signin/", views.login_view, name="sign-in"),
    path("logout/", views.logout_view, name="logout"),
]

app_name = "userauths"
