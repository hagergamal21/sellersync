from django.urls import path
from . import views




urlpatterns = [
    path('', views.HomePage, name='home'),
    path('login/' , views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('register/' , views.RegisterPage, name='register'),
    path('home/' , views.home, name='home2'),
    


]


from django.urls import path
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
