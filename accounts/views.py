from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, LoginForm

# Signup 

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip()
            password = form.cleaned_data["password1"]

            # Split full name into first / last
            name_parts = full_name.split()
            first_name = name_parts[0] if name_parts else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            login(request, user, backend="accounts.backends.EmailOrUsernameBackend")

            # Welcome the new user
            first = user.first_name or user.username
            messages.success(request, f"Welcome to VibeStream, {first}!")

            return redirect("home")

        # Form has errors – re-render with error messages
        return render(request, "movies/signup.html", {"form": form})

    # GET – show empty form
    return render(request, "movies/signup.html", {"form": SignupForm()})


# Login 


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # The custom EmailOrUsernameBackend handles email-or-username lookup
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user, backend="accounts.backends.EmailOrUsernameBackend")

                first = user.first_name or user.username
                messages.success(request, f"Welcome back, {first}!")

                next_url = request.POST.get("next") or request.GET.get("next") or "home"
                return redirect(next_url)

        return render(request, "movies/login.html", {
            "form": form,
            "error": "Invalid username/email or password.",
            "next": request.GET.get("next", ""),
        })

    return render(request, "movies/login.html", {
        "form": LoginForm(),
        "next": request.GET.get("next", ""),
    })


# =========================
# Logout
# =========================

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")


# =========================
# Check if user exists 
# =========================

def check_user(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()

        exists = (
            User.objects.filter(username=identifier).exists()
            or User.objects.filter(email=identifier).exists()
        )

        return JsonResponse({"exists": exists})

    return JsonResponse({"exists": False})

# =========================
# Settings
# =========================

@login_required
def settings_view(request):
    return render(request, "movies/profile.html")


# =========================
# Delete Account
# =========================

@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password", "")

        # Verify current password
        if not request.user.check_password(password):
            messages.error(request, "Incorrect password.")
            return redirect("settings")

        # Delete account
        user = request.user
        username = user.first_name or user.username

        logout(request)
        user.delete()
        messages.success(
            request,
            f"Your VibeStream account has been permanently deleted. Goodbye, {username}."
        )

        return redirect("home")

    return redirect("settings")
    # =========================
# Edit Profile
# =========================

@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()

        name_parts = full_name.split()

        user.first_name = name_parts[0] if name_parts else ""
        user.last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        user.email = email

        user.save()

        messages.success(
            request,
            "Your profile has been updated successfully."
        )

        return redirect("settings")

    return render(request, "movies/profile.html")
