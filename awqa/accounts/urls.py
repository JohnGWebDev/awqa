from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView, UserProfileDeleteView

urlpatterns = [
    
    path('<int:pk>/profile/', UserProfileDetailView.as_view(), name='user-profile'),
    path('<int:pk>/profile/update/', UserProfileUpdateView.as_view(), name='update-user-profile'),
    path('<int:pk>/profile/delete/', UserProfileDeleteView.as_view(), name='delete-user-profile'),

]