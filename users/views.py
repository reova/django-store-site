from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)  # creating a form with user data

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(
                username=username, password=password
            )  # check if the user is in the db

            if user:
                auth.login(request, user)  # if the user is in the db - authorize
                messages.success(request, f"{username}, вошли в аккаунт")

                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Авторизация",
        "form": form,
    }

    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            user = form.instance  # get data from form
            auth.login(request, user)  # authorize user
            messages.success(request, f"{user.username}, успешно зарегистрировались и вошли в аккаунт")

            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Регистрация",
        "form": form,
    }

    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(request, f"Профиль успешно обновлен")

            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "Кабинет",
        "form": form,
    }

    return render(request, "users/profile.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, ливнул в аккаунта")
    auth.logout(request)

    return redirect(reverse("main:index"))
