from django.contrib import admin
from django.urls import path,include
from .views import LandingPageView, PrivacyPolicyView, DashboardView
from accounts.views import UserCoreSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('water_quality_management.urls', 'water_quality_management'))),
    path('', LandingPageView.as_view(), name="index"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name="privacy-policy"),
    path('accounts/signup/', UserCoreSignupView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('tz_detect/', include('tz_detect.urls')),
    path('payments/', include(('payments.urls', 'payments'))),
]
