from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from allauth.account.views import SignupView
from .forms import UserCoreSignupForm
from django_htmx.http import retarget, reswap, _HttpResponse
from django.http import HttpResponse
from core.mixins import PrivatePageMixin

# Create your views here.
User = get_user_model()

class UserCoreSignupView(SignupView):
    form = UserCoreSignupForm
    

class UserProfileDetailView(PrivatePageMixin, LoginRequiredMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs["pk"])
        context["aquarium_list"] = user.aquarium_set.order_by("-last_updated")[:5]
        context["log_entry_list"] = user.freshwaterparameterlogentry_set.order_by("-last_updated")[:5]
        return context


class UserProfileUpdateView(PrivatePageMixin, LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name')


class UserProfileDeleteView(PrivatePageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("index")
