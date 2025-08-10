from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from mailing.forms import MailingForm, MailingUpdateForm
from mailing.models import Mailing
from mailing.services import start_sending_message


# @method_decorator(cache_page(60 * 15), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing.html"

    # def get_queryset(self):
    #     user = self.request.user
    #     # user.groups.filter(name='Managers').exists()
    #     if user.is_superuser or user.has_perm("mailing.can_all_view_mailing"):
    #         return Mailing.objects.all()
    #     return Mailing.objects.filter(owner=user.pk)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "create_mailing.html"
    success_url = reverse_lazy("mailing:mailing")

    def form_valid(self, form):
        mailing: Mailing = form.save(commit=False)
        user = self.request.user
        if user.is_superuser or user.has_perm("mailing.can_create_mailing"):
            mailing.owner = self.request.user
            mailing.save()
            form.save_m2m()
            start_sending_message(mailing)
            return super().form_valid(form)
        raise PermissionDenied


class MailingDetailView(DetailView):
    pass


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "delete_mailing.html"
    success_url = reverse_lazy("mailing:mailing")

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.has_perm("mailing.can_delete_mailing"):
            return super().delete(request, *args, **kwargs)
        raise PermissionDenied


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingUpdateForm
    template_name = "update_mailing.html"
    success_url = reverse_lazy("mailing:mailing")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user

        if (
            user.is_superuser
            or user.has_perm("mailing.can_update_mailing")
            or mailing.owner == self.request.user
        ):
            mailing.save()
            return super().form_valid(form)
        raise PermissionDenied
