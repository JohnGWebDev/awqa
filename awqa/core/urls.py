from django.contrib import admin
from django.urls import path,include
from .views import LandingPageView, PrivacyPolicyView, DashboardView, FeedbackView, TOSView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('water_quality_management.urls')),
    path('', LandingPageView.as_view(), name="index"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name="privacy-policy"),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]
