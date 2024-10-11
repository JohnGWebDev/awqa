from django.urls import path
from . import views


urlpatterns = [
    path('aquarium/create/', views.AquariumCreateView.as_view(), name='create-aquarium'),
    path('aquarium/<int:pk>/', views.AquariumDetailView.as_view(), name='aquarium-detail'),
    path('aquarium/<int:pk>/update', views.AquariumUpdateView.as_view(), name='update-aquarium'),
    path('aquarium/<int:pk>/delete/', views.AquariumDeleteView.as_view(), name='delete-aquarium'),

    path('accounts/<int:pk>/aquarium/list/', views.AquariumListView.as_view(), name='aquarium-list'),

    path('aquarium/<int:pk>/log-entry/create/', views.WaterQualityLogEntryCreateView.as_view(), name="add-log-entry"),
    path('log-entry/<int:pk>/', views.WaterQualityLogEntryDetailView.as_view(), name="log-entry-detail"),
    path('log-entry/<int:pk>/update/', views.WaterQualityLogEntryUpdateView.as_view(), name='update-log-entry'),
    path('log-entry/<int:pk>/delete/', views.WaterQualityLogEntryDeleteView.as_view(), name='delete-log-entry'),

    path('accounts/<int:pk>/log-entry/list/', views.WaterQualityLogEntryListView.as_view(), name='log-entry-list'),
]