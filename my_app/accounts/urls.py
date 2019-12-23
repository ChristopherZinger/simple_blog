from django.urls import path
from django.contrib.auth.views import (
    PasswordResetConfirmView, PasswordResetView
)
from accounts.views import (
user_login , user_logout,
user_home, user_create, user_info_update,
user_update
)



app_name = 'accounts'

urlpatterns=[
    path('<slug:user_slug>', user_home, name='user_home'),
    # Authorisation
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_create, name='user_create'),
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_email.html'), name='password_reset'),
    path('info_update/<slug:user_slug>', user_info_update, name='user_info_update'),
    path('user_update/<slug:user_slug>', user_update, name='user_update'),



]


# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
