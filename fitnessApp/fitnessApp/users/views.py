from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DeleteView
from django.contrib import messages
from django.contrib.auth import login

from fitnessApp.users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from fitnessApp.users.models import UserProfile


class AppUserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        messages.success(self.request, 'Your account has been created!')
        return response


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.user_profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(self.request, 'Your profile has been updated!')
            return redirect('profile')

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'users/profile.html', context)


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'users/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(UserProfile, pk=self.kwargs["pk"])
        return self.request.user == profile.user

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=self.kwargs["pk"])
        context = {'profile': profile}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=self.kwargs["pk"])
        user = profile.user

        user.delete()
        profile.delete()

        return redirect(self.success_url)
