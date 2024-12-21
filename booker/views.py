from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    return render(request, 'delete-profile.html')
