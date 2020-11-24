from django.urls import path
from homepage import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
app_name='homepage'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('password_reset/',PasswordResetView.as_view(),name="password_reset"),
    path('password_reset_done/',PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password_reset_confirm/',PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('feedback/',views.user_feedback,name="user_feedback"),
]
