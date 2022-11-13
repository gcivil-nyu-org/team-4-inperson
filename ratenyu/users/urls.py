from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="search/index.html"),
        name="logout",
    ),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
            email_template_name="users/email_template.html",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_form.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/<str:user_name>", views.get_profile, name="profile"),
    path("profile/<str:user_name>/edit_profile", views.edit_profile, name="editProfile"),
]
