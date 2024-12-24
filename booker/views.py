from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# For the button
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from booker.forms import AccountForm


def index(request):
    return render(request, "index.html", {"user": request.user})


# @login_required
def all_bookings(request):
    return render(request, "all-bookings.html")


@login_required
def create_booking(request):
    # Logic for creating a booking
    return render(request, "create-booking.html")


def login_view(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        # print(f"Nickname: {nickname}, Password: {password}")
        user = authenticate(request, nickname=nickname, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('all-bookings')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")


def create_profile(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()  # Save the account instance
            user = authenticate(request, username=account.nickname, password=request.POST['password'])
            if user:
                login(request, user)
                messages.success(request, "Profile created successfully, and you are now logged in!")
                return redirect('all-bookings')
            else:
                messages.error(request, "An error occurred during login. Please log in manually.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountForm()

    return render(request, "create-profile.html", {'form': form})


def profile(request):
    return render(request, 'details-profile.html')


# def edit_profile(request):
#     return render(request, 'edit-profile.html')

def upload_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile_picture = request.FILES["profile_picture"]

        # Validate file size (10MB = 10 * 1024 * 1024 bytes)
        if profile_picture.size > 10 * 1024 * 1024:
            messages.error(request, "File size must not exceed 10MB.")
            return redirect("profile")

        # Update user's profile picture
        request.user.profile_picture = profile_picture
        request.user.save()
        messages.success(request, "Profile picture updated successfully!")
        return redirect("profile")

    return redirect("profile")


@csrf_exempt
def update_phone_number(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number")

            # Validate phone number (optional)
            if not phone_number.isdigit() or len(phone_number) != 10:
                return JsonResponse({"error": "Invalid phone number."}, status=400)

            user = request.user
            user.phone_number = phone_number
            user.save()

            return JsonResponse({"phone_number": user.phone_number})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)
