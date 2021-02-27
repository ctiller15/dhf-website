from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm

def dashboard(request):
    return render(request, "users/dashboard.html")

def login_route(request):
    if request.method == 'POST':
       form = AuthenticationForm(request.POST)
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(username=username, password=password)
       if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("dashboard"))
            else:
                messages.error(request, 'username or password not correct')
                return redirect(reverse("login_route"))

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form, 'extra': { 'hide_search_bar': True }})

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm, 
             "extra": { 'hide_search_bar': True}}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # Handle if form is not valid.
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))
