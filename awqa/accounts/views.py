from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.
User = get_user_model()


class UserProfileDetailView(DetailView, LoginRequiredMixin):
    model = User

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.is_private:
            if object != self.request.user:
                if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                    raise PermissionDenied
        if object.is_active == False:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs["pk"])
        context["aquarium_list"] = user.aquarium_set.order_by("-last_updated")[:5]
        context["log_entry_list"] = user.freshwaterparameterlogentry_set.order_by("-last_updated")[:5]
        return context
    


class UserProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'is_private')

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object != self.request.user:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return object


class UserProfileDeleteView(DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object != self.request.user:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return object