from django.urls import path
from user.views import UserSignupView, LoginView
from .views import AddToCartView, DetailProfileView, CartView, LogoutView,  PasswordResetRequestView, PasswordResetConfirmView

app_name = 'user'

urlpatterns = [
    path('register/',UserSignupView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-item-delete'),
    path('userprofile/', DetailProfileView.as_view(), name= 'detailView'),
    path('logout/', LogoutView.as_view(), name = 'logout' ),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]





