from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from contests.models import Domain
from users.models import Profile
from users.permissions import check_staff


@login_required
def dashboard(request):
    if not hasattr(request.user, 'profile'):
        return redirect(create_profile)
    if check_staff(request.user):
        return redirect('view-contests')
    else:
        return redirect('view-contests-student')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            try:
                user = User.objects.get(email=username)
            except:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'login.html')
        isvalid = auth.authenticate(request, username=user.username, password=pwd)
        if isvalid:
            auth.login(request, isvalid)
            return redirect(dashboard)
        messages.error(request, 'Invalid Credentials')
    if request.user.is_authenticated:
        return redirect(dashboard)
    return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def create_profile(request):
    if hasattr(request.user, 'profile'):
        return redirect(dashboard)
    if request.method == 'POST':
        type = int(request.POST.get('type'))
        password = request.POST.get('password')
        domains = request.POST.get('domains').split(';')
        user = request.user
        user.set_password(password)
        profile = Profile.objects.create(user=user, type=type)
        for domain in domains:
            profile.domains.add(Domain.objects.get(name=domain))
        profile.save()
        return redirect(dashboard)
    return render(request, 'users/create_profile.html', {'title': 'Welcome', 'heading': 'Profile Updation'})
