from django.urls import path
from . import views



urlpatterns = [
    path('checkout/<int:pk>/', views.CheckoutView.as_view(), name='checkout'),
    path('create-checkout-session/<int:pk>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('session-status/', views.SessionStatusView.as_view(), name='session-status'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),

]