from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is organisor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_organisor:
            return HttpResponseRedirect(reverse("leads:list"))
        return super().dispatch(request, *args, **kwargs)