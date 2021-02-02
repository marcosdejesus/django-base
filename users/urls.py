from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.signup, {'redirect_url': 'notifier:home'},
         name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view()),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name = 'login'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name = 'users/password_reset.html',
            email_template_name = 'users/password_reset_email.html',
            subject_template_name = 'users/password_reset_subject.txt',
            success_url = 'done/'
            ),
        name = 'password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name = 'users/password_reset_done.html'),
         name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name = 'users/password_reset_confirm.html'),
         name = 'password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name = 'users/password_reset_complete.html'),
         name = 'password_reset_complete'),
#    path('password_change/',
#         auth_views.PasswordChangeView.as_view(
#             template_name = 'users/password_change.html',
#             success_url = 'done/'),
#         name = 'password_change'),
#    path('password_change/done/',
#         auth_views.PasswordChangeDoneView.as_view(
#             template_name = 'users/password_change_done.html'),
#         name = 'password_change_done'),
]
