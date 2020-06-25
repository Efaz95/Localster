from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CreateProfileForm, UpdateProfileForm
from .models import InfluencerProfile


def register(request):
    form = CreateProfileForm()

    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='influencer')
            user.groups.add(group)

            InfluencerProfile.objects.create(user=user)

            first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Account successfully created for ' + first_name)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def home(request):
    return render(request, 'accounts/home.html')


def account(request, un):
    influencer = InfluencerProfile.objects.get(user__username=un)

    form = UpdateProfileForm(instance=influencer)

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=influencer)
        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'influencer': influencer, 'form': form}
    return render(request, 'accounts/home.html', context)
