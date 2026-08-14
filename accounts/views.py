from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# =========================
# Signup (Email or Username)
# =========================

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "movies/signup.html", {
                "error": "Passwords do not match."
            })

        base_username = email.split("@")[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("home")

    return render(request, "movies/signup.html")


# =========================
# Login (Email or Username)
# =========================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "movies/login.html", {
            "error": "Invalid username/email or password."
        })

    return render(request, "movies/login.html")


# =========================
# Logout
# =========================

def logout_view(request):
    logout(request)
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
# Edit Profile
# =========================

@login_required
def edit_profile(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()

        # Check if username is already used by another user
        if (
            User.objects.filter(username=username)
            .exclude(id=request.user.id)
            .exists()
        ):
            return render(
                request,
                "accounts/edit_profile.html",
                {
                    "error": "Username already exists."
                },
            )

        request.user.username = username
        request.user.email = email
        request.user.save()

        return redirect("profile")

    return render(
        request,
        "accounts/edit_profile.html",
    )