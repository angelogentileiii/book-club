from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView

from .forms.signup_form import SignUpForm
from .models import UserProfile

# Create your views here.


class SignUpView(CreateView):
    model = UserProfile
    form_class = SignUpForm
    template_name = "users/user-signup.html"
    success_url = reverse_lazy("home_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["signup_form"] = self.get_form()
        return context

    def form_valid(self, form):
        # Encrypt password before saving the user
        user = form.save(commit=False)

        user.address = form.cleaned_data["address"]  # Set the cleaned address
        user.set_password(form.cleaned_data["password"])  # Set the password hash

        user.save()

        # Log the user in after signup
        login(self.request, user)

        # Redirect to the success URL after successful signup
        return super().form_valid(form)
