from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django import template
from django.contrib.auth.models import User
from .forms import CreateProfileForm, UpdateInfProfileForm, UpdateBisProfileForm, MessagesForm
from .models import InfluencerProfile, BusinessProfile, Messages, Hire
import datetime


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
            return redirect('/')
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
    user = request.user

    searched_inf = None
    if request.method == "POST":
        if 'hired_influencer' in request.POST:
            hired_by = request.user
            hired_inf = request.POST.get('hired_influencer')
            hired_inf1 = User.objects.get(username=hired_inf)
            Hire.objects.create(hired_by=hired_by, hired_influencer=hired_inf1)
        if 'unhired_id' in request.POST:
            unhired_id = request.POST.get('unhired_id')
            Hire.objects.get(id=unhired_id).delete()
        else:
            user_zip = user.businessprofile.zip_code
            searched_inf = InfluencerProfile.objects.filter(zip_code=user_zip)

    hired_by_this_business = Hire.objects.filter(hired_by=request.user.id)
    working_with = Hire.objects.filter(hired_influencer=request.user.id)

    context = {'user': user, 'searched_inf': searched_inf,
               'hired_by_this_business': hired_by_this_business, 'working_with': working_with}

    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
def account_settings(request, un):
    group = Group.objects.get(user__username=un)

    if group.name == "influencer":
        influencer = InfluencerProfile.objects.get(user__username=un)
        form = UpdateInfProfileForm(instance=influencer)

        if request.method == "POST":
            form = UpdateInfProfileForm(request.POST, instance=influencer)
            if form.is_valid():
                form.save()

                return redirect('home')

        context = {'influencer': influencer, 'form': form}
        return render(request, 'accounts/settings.html', context)

    elif group.name == "business":
        business = BusinessProfile.objects.get(user__username=un)
        form = UpdateBisProfileForm(instance=business)

        if request.method == "POST":
            form = UpdateBisProfileForm(request.POST, instance=business)
            if form.is_valid():
                form.save()

                return redirect('home')

        context = {'business': business, 'form': form}
        return render(request, 'accounts/settings.html', context)


@login_required(login_url='login')
def user_messages(request):
    time_now = datetime.datetime.now()
    user = request.user

    if request.method == "POST":
        if 'read' in request.POST:
            un = request.POST.get('read')
            Messages.objects.filter(id=un).update(is_read=True)
        else:
            sender = request.user
            receiver_name = request.POST.get('msg_receiver')
            receiver = User.objects.get(username=receiver_name)
            msg_content = request.POST.get('msg_content')

            Messages.objects.create(sender=sender, receiver=receiver, msg_content=msg_content)

    inbox = Messages.objects.filter(receiver=user).order_by('-timestamp')
    outbox = Messages.objects.filter(sender=user).order_by('-timestamp')

    context = {'inbox': inbox, 'outbox': outbox, 'time_now': time_now}

    return render(request, 'accounts/messages.html', context)


@login_required(login_url='login')
def msgs_json(request):
    user = request.user

    inbox = Messages.objects.filter(receiver=user).order_by('-timestamp')
    serialized_inbox = serializers.serialize('json', inbox)

    return HttpResponse(serialized_inbox, content_type='application/json')
