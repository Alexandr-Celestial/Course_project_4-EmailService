import secrets

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, response
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.defaults import permission_denied
from django.views.generic import CreateView, ListView, DeleteView

from config.settings import EMAIL_HOST_USER
from user.models import User


def login_user(request: HttpRequest):
    check_post = request.POST
    if check_post:
        email = check_post.get("email-username")
        password = check_post.get("password")
        user = auth.authenticate(request, email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect(reverse("recipients:recipients"))
        else:
            return permission_denied(request, ValueError)
    return render(request, "auth.html")

def logout_user(request):
    logout(request)
    return redirect(reverse("recipients:recipients"))

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in self._meta.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)

class CreateUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('recipients:recipients')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()

        url = f'http://{self.request.get_host()}/user/valid_token/{user.token}'
        print(url)
        send_mail('Предоставление доступа',
                  f'Пожалуйста перейдите на {url}',
                  EMAIL_HOST_USER,
                  [user.email])
        return super().form_valid(form)

def validation_user(requests, token):
    user: User = get_object_or_404(User, token=token)
    if not user: return PermissionDenied
    user.is_active = True
    user.is_staff = True
    user.save()
    return redirect('recipients:recipients')

class UserListView(ListView):
    model = User
    template_name = "users_services.html"

    def get_queryset(self):
        user = self.request.user
        # user.groups.filter(name='Managers').exists()
        if user.is_superuser or user.has_perm("user.view_user"):
            return User.objects.all()
        return User.objects.filter(owner=user.pk)

def block_user(request: HttpRequest, pk):
    user: User = get_object_or_404(User, id=pk)
    if not user: return PermissionDenied
    user.is_active = not user.is_active
    user.save()
    return HttpResponse('ок')
