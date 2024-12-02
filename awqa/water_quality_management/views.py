from datetime import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from django.contrib.messages.views import SuccessMessageMixin
from core.mixins import OptionallyPrivateObjectMixin, PrivatePageMixin
from .models import Aquarium, FreshWaterParameterLogEntry
from .forms import AquariumForm, FreshWaterParamaterLogEntryForm

User = get_user_model()


# When creating a new aquarium object, we can assume the current
# user will be the owner, and the date fields will be automatically populated.
class AquariumCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Aquarium
    form_class = AquariumForm
    success_message = "New aquarium was added successfully!"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.aquarium_set.count() >= self.request.user.max_aquariums:
            messages.error(request, "You have reached your maximum number of aquariums.")
            return redirect(reverse("dashboard"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.can_create_aquarium == False:
            raise PermissionDenied
        form.instance.user = self.request.user
        return super(AquariumCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.request.user.pk})},
            {'name': 'Add Aquarium'},
        ]
        context["breadcrumbs"] = pages
        return context
    


# This view displays a chart using Plotly. I created a function that
# returns the last 30 days of log entry data in json format for Plotly to consume.
class AquariumDetailView(PrivatePageMixin, LoginRequiredMixin, DetailView):
    model = Aquarium

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object.freshwaterparameterlogentry_set.all().order_by('-date_created'), 5)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)

        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.name },
        ]
        context["breadcrumbs"] = pages
        return context



# If a user's profile is set to private, only they may view their aquarium list.
# If a user's profile is set to public, we must still restrict aquarium objects set to private.
class AquariumListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        users_active_aquariums = Aquarium.objects.filter(is_active=True).filter(user=user).order_by('-date_created')
        if user != self.request.user:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return users_active_aquariums
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List'},
        ]
        context["breadcrumbs"] = pages
        return context


# When updating an aquarium object, only the owner, staff and superusers should have access to this page.
# The last_updated field will be populated automatically.
class AquariumUpdateView(SuccessMessageMixin, PrivatePageMixin, LoginRequiredMixin, UpdateView):
    model = Aquarium
    form_class = AquariumForm
    template_name = 'water_quality_management/aquarium_update_form.html'
    success_message = "Your aquarium was updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':self.object.pk})},
            {'name': 'Update Aquarium'}
        ]
        context["breadcrumbs"] = pages
        return context
    


# When deleting an aquarium object, only the owner, staff and superusers should have access to this page.
class AquariumDeleteView(SuccessMessageMixin, PrivatePageMixin, LoginRequiredMixin, DeleteView):
    model = Aquarium
    success_url = reverse_lazy('dashboard')
    success_message = "Your aquarium was deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':self.object.pk})},
            {'name': 'Delete Aquarium'}
        ]
        context["breadcrumbs"] = pages
        return context


# When creating a new log entry object, we can assume the current
# user will be the owner, and the date fields will be automatically populated.
# The aquarium object owner is the only one who should be able to view this page.
# We must use the aquarium pk we passed through kwargs to retrieve the correct object instance.
# Then pass that object to the aquarium field in our form instance.
class WaterQualityLogEntryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = FreshWaterParameterLogEntry
    form_class = FreshWaterParamaterLogEntryForm
    success_message = "New log entry was added successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aquarium"] = Aquarium.objects.get(pk=self.kwargs['pk'])
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':context['aquarium'].user.pk})},
            {'name': context['aquarium'].name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':context['aquarium'].pk})},
            {'name': 'Add Log Entry'}
        ]
        context["breadcrumbs"] = pages
        if context["aquarium"].user != self.request.user:
            raise PermissionDenied
        return context
    
    def form_valid(self, form):
        form.instance.aquarium = Aquarium.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.aquarium.last_updated = datetime.now()
        form.instance.aquarium.save()
        return super(WaterQualityLogEntryCreateView, self).form_valid(form)


# Super straight-forward DetailView, see comments on custom mixin for more info.
class WaterQualityLogEntryDetailView(PrivatePageMixin, LoginRequiredMixin, DetailView):
    model = FreshWaterParameterLogEntry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.aquarium.name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':self.object.aquarium.pk})},
            {'name': self.object.date_created}
        ]
        context["breadcrumbs"] = pages
        return context


# When updating an entry log object, only the owner, staff and superusers should have access to this page.
# The last_updated field will be populated automatically.
class WaterQualityLogEntryUpdateView(SuccessMessageMixin, PrivatePageMixin, LoginRequiredMixin, UpdateView):
    model = FreshWaterParameterLogEntry
    form_class = FreshWaterParamaterLogEntryForm
    template_name = 'water_quality_management/freshwaterparameterlogentry_update_form.html'
    success_message = "Your log entry was updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.aquarium.name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':self.object.aquarium.pk})},
            {'name': self.object.date_created, 'url': reverse('water_quality_management:log-entry-detail', kwargs={'pk': self.object.pk})},
            {'name': 'Update Log Entry'}
        ]
        context["breadcrumbs"] = pages
        return context


# When deleting an aquarium object, only the owner, staff and superusers should have access to this page.
class WaterQualityLogEntryDeleteView(SuccessMessageMixin, PrivatePageMixin, LoginRequiredMixin, DeleteView):
    model = FreshWaterParameterLogEntry
    success_url = reverse_lazy("dashboard")
    success_message = "Your log entry was deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Aquarium List', 'url': reverse('water_quality_management:aquarium-list', kwargs={'pk':self.object.user.pk})},
            {'name': self.object.aquarium.name, 'url': reverse('water_quality_management:aquarium-detail', kwargs={'pk':self.object.aquarium.pk})},
            {'name': self.object.date_created, 'url': reverse('water_quality_management:log-entry-detail', kwargs={'pk': self.object.pk})},
            {'name': 'Delete Log Entry'}
        ]
        context["breadcrumbs"] = pages
        return context


# If a user's profile is set to private, only they may view their log entry list.
# If a user's profile is set to public, we must still restrict log entry objects set to private.
class WaterQualityLogEntryListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        users_active_log_entries = FreshWaterParameterLogEntry.objects.filter(is_active=True).filter(user=user).order_by('-date_created')
        if user != self.request.user:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return users_active_log_entries
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pages = [
            {'name': 'Dashboard', 'url': reverse('dashboard')},
            {'name': 'Log Entry List'},
        ]
        context["breadcrumbs"] = pages
        return context

    