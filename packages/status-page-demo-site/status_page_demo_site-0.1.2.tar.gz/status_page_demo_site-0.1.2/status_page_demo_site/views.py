import random
import string
from random import randrange

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.views.generic import View

from status_page_demo_site.forms import DemoLoginForm


class LoginView(View):
    template_name = "demo_login.html"

    def get(self, request):
        form = DemoLoginForm()

        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, self.template_name, {
            'request': request,
            'form': form,
        })

    def post(self, request):
        form = DemoLoginForm(data=request.POST)

        if form.is_valid():
            last_user = User.objects.last()

            if not last_user:
                last_user_id = 0
            else:
                last_user_id = last_user.id

            letters = string.ascii_letters
            default_password = ''.join(random.choice(letters) for i in range(12))

            username = request.POST.get('username')
            if not username:
                username = f'user{last_user_id+randrange(1000, 10001)}'
            password = request.POST.get('password')
            if not password:
                password = default_password

            user = authenticate(
                self.request, username=username, password=password
            )
            if user is None:
                user = User.objects.create_user(username=username, password=password, is_staff=True, is_superuser=False)
                demo_group = Group.objects.get(name='demo-admin')
                demo_group.user_set.add(user)

            login(request, user)
            messages.info(request, f"Logged in as {username} with {password}")

            return redirect('dashboard')

        messages.warning(request, f"Validation failed")

        return render(request, self.template_name, {
            'request': request,
            'form': form,
        })
