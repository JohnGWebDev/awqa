from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin

# If an object is set to private or a users profile is set to private, only its owner, staff, and superusers should be able to view it.
# If a user sets their profile to private or it is set to inactive, only staff and superusers should be able to view the object.
class OptionallyPrivateObjectMixin(LoginRequiredMixin, SingleObjectMixin):

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.user.is_private or object.is_private:
            if object.user != self.request.user:
                if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                    raise PermissionDenied
        if object.user.is_active == False:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return object
    

class PrivatePageMixin(LoginRequiredMixin, SingleObjectMixin):

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object != self.request.user and object.user != self.request.user:
            if self.request.user.is_staff == False and self.request.user.is_superuser == False:
                raise PermissionDenied
        return object