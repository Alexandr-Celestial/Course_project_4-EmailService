from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from recipients.forms import RecipientForm
from recipients.models import Recipient


# @method_decorator(cache_page(60 * 15), name="dispatch")
class RecipientsListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipients.html"

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser or user.has_perm("recipients.can_all_view_recipients"):
    #         return Recipient.objects.all()
    #     return Recipient.objects.filter(owner=user.pk)


class RecipientsCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "create_recipient.html"
    success_url = reverse_lazy("recipients:recipients")

    def form_valid(self, form):
        message = form.save(commit=False)
        user = self.request.user
        if user.is_superuser or user.has_perm("recipients.can_create_recipient"):
            message.owner = user
            message.save()
            return super().form_valid(form)
        raise PermissionDenied


class RecipientsDetailView(DetailView):
    pass


class RecipientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "delete_recipient.html"
    success_url = reverse_lazy("recipients:recipients")

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.has_perm("recipients.can_delete_recipient"):
            return super().delete(request, *args, **kwargs)
        raise PermissionDenied


class RecipientsUpdateView(UpdateView):
    pass
