from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib import messages
from django import template
from django.contrib.auth.models import User
from .forms import CreateProfileForm, UpdateInfProfileForm, UpdateBisProfileForm
from .models import InfluencerProfile, BusinessProfile


def register(request):
    form = CreateProfileForm()

    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            user = form.save()

            group1 = request.POST['groups']
            group = Group.objects.get(name=group1)
            user.groups.add(group)

            if group1 == 'influencer':
                InfluencerProfile.objects.create(user=user)
            else:
                BusinessProfile.objects.create(user=user)

            first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Account successfully created for ' + first_name)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/account/{username}')
        else:
            messages.info(request, "User and/or Password is incorrect")
            return render(request, 'accounts/login.html')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/home.html')


@login_required(login_url='login')
def account(request, un):
    group = Group.objects.get(user__username=un)
    print(f"🔥🔥🔥🔥  {group}")

    if str(group) == "influencer":
        influencer = InfluencerProfile.objects.get(user__username=un)
        form = UpdateInfProfileForm(instance=influencer)

        if request.method == "POST":
            form = UpdateInfProfileForm(request.POST, instance=influencer)
            if form.is_valid():
                form.save()

                return redirect('home')

        context = {'influencer': influencer, 'form': form}
        return render(request, 'accounts/home.html', context)

    elif str(group) == "business":
        business = BusinessProfile.objects.get(user__username=un)
        form = UpdateBisProfileForm(instance=business)

        if request.method == "POST":
            form = UpdateBisProfileForm(request.POST, instance=business)
            if form.is_valid():
                form.save()

                return redirect('home')

        context = {'business': business, 'form': form}
        return render(request, 'accounts/home.html', context)
