from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from core.mixins import OptionallyPrivateObjectMixin, PrivatePageMixin
from .models import Aquarium, FreshWaterParameterLogEntry

import json

User = get_user_model()


# When creating a new aquarium object, we can assume the current
# user will be the owner, and the date fields will be automatically populated.
class AquariumCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aquarium
    fields = ('name', 'is_private',)
    success_message = "New aquarium was added successfully!"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.aquarium_set.count() >= self.request.user.max_aquariums:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
        
    

    def form_valid(self, form):
        if self.request.user.can_create_aquarium == False:
            raise PermissionDenied
        form.instance.user = self.request.user
        return super(AquariumCreateView, self).form_valid(form)


# This view displays a chart using Plotly. I created a function that
# returns the last 30 days of log entry data in json format for Plotly to consume.
class AquariumDetailView(DetailView, OptionallyPrivateObjectMixin):
    model = Aquarium

    def get_chart_data_json(self):
        # Get the last 30 days of entries.
        now = timezone.now()
        last_thirty_days = now - timedelta(days=30)
        log_entry_list = self.object.freshwaterparameterlogentry_set.filter(date_created__range=(last_thirty_days, now))
        # Only show private entries if the current user is the owner.
        if self.object.user != self.request.user:
            log_entry_list.filter(is_private=False)
        # Serialize into json and return when function is called.
        data = serializers.serialize('json', log_entry_list)
        data = json.loads(data)
        return data

    # Pass chart data in detail view context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = self.get_chart_data_json
        return context


# If a user's profile is set to private, only they may view their aquarium list.
# If a user's profile is set to public, we must still restrict aquarium objects set to private.
class AquariumListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        users_active_aquariums = Aquarium.objects.filter(is_active=True).filter(user=user)
        if user != self.request.user:
            users_active_aquariums = users_active_aquariums.filter(is_private=False)
        return users_active_aquariums
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_owner'] = User.objects.get(pk=self.kwargs['pk'])
        if context['list_owner'].is_private:
            if context['list_owner'] != self.request.user:
                if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                    raise PermissionDenied
        if context['list_owner'].is_active == False:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        if context['list_owner'] == self.request.user:
            context['list_owner'] = None
        return context


# When updating an aquarium object, only the owner, staff and superusers should have access to this page.
# The last_updated field will be populated automatically.
class AquariumUpdateView(UpdateView, SuccessMessageMixin, PrivatePageMixin):
    model = Aquarium
    fields = ('name', 'is_private',)
    template_name = 'water_quality_management/aquarium_update_form.html'
    success_message = "Your aquarium was updated successfully!"


# When deleting an aquarium object, only the owner, staff and superusers should have access to this page.
class AquariumDeleteView(DeleteView, SuccessMessageMixin, PrivatePageMixin):
    model = Aquarium
    success_url = reverse_lazy('dashboard')
    success_message = "Your aquarium was deleted successfully!"


# When creating a new log entry object, we can assume the current
# user will be the owner, and the date fields will be automatically populated.
# The aquarium object owner is the only one who should be able to view this page.
# We must use the aquarium pk we passed through kwargs to retrieve the correct object instance.
# Then pass that object to the aquarium field in our form instance.
class WaterQualityLogEntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FreshWaterParameterLogEntry
    fields = ('is_private', 'ph', 'high_range_ph', 'ammonia', 'nitrite', 'nitrate',)
    success_message = "New log entry was added successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aquarium"] = Aquarium.objects.get(pk=self.kwargs['pk'])
        if context["aquarium"].user != self.request.user:
            raise PermissionDenied
        return context
    
    def form_valid(self, form):
        form.instance.aquarium = Aquarium.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super(WaterQualityLogEntryCreateView, self).form_valid(form)


# Super straight-forward DetailView, see comments on custom mixin for more info.
class WaterQualityLogEntryDetailView(DetailView, OptionallyPrivateObjectMixin):
    model = FreshWaterParameterLogEntry


# When updating an entry log object, only the owner, staff and superusers should have access to this page.
# The last_updated field will be populated automatically.
class WaterQualityLogEntryUpdateView(UpdateView, SuccessMessageMixin, PrivatePageMixin):
    model = FreshWaterParameterLogEntry
    fields = ('is_private', 'ph', 'high_range_ph', 'ammonia', 'nitrite', 'nitrate',)
    template_name = 'water_quality_management/freshwaterparameterlogentry_update_form.html'
    success_message = "Your log entry was updated successfully!"


# When deleting an aquarium object, only the owner, staff and superusers should have access to this page.
class WaterQualityLogEntryDeleteView(DeleteView, SuccessMessageMixin, PrivatePageMixin):
    model = FreshWaterParameterLogEntry
    success_url = reverse_lazy("aquarium-list")
    success_message = "Your log entry was deleted successfully!"


# If a user's profile is set to private, only they may view their log entry list.
# If a user's profile is set to public, we must still restrict log entry objects set to private.
class WaterQualityLogEntryListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        users_active_log_entries = FreshWaterParameterLogEntry.objects.filter(is_active=True).filter(user=user)
        if user != self.request.user:
            users_active_log_entries = users_active_log_entries.filter(is_private=False)
        return users_active_log_entries
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_owner'] = User.objects.get(pk=self.kwargs['pk'])
        if context['list_owner'].is_private:
            if context['list_owner'] != self.request.user:
                if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                    raise PermissionDenied
        if context['list_owner'].is_active == False:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        if context['list_owner'] == self.request.user:
            context['list_owner'] = None
        return context

    