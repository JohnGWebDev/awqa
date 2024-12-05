from typing import Any
from django.shortcuts import redirect
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from payments.models import Product


class LandingPageView(TemplateView):
    template_name = "core/index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["aquarium_list"] = self.request.user.aquarium_set.order_by("-last_updated")[:5]
        context["log_entry_list"] = self.request.user.freshwaterparameterlogentry_set.order_by("-last_updated")[:5]
        context["product_1_pk"] = Product.objects.get(title="One Extra Aquarium Slot").pk
        return context
    
    
class PrivacyPolicyView(TemplateView):
    template_name = "core/privacy_policy.html"

class TOSView(TemplateView):
    template_name = "core/tos.html"

class FeedbackView(TemplateView):
    template_name = "core/feedback.html"