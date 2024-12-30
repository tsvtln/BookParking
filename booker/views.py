from calendar import monthrange
from datetime import datetime

from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# For the button
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from booker.forms import AccountForm, BookingForm
from booker.models import Booking, Account, ParkingAvailability


def index(request):
    return render(request, "index.html", {"user": request.user})


# @login_required
def all_bookings(request):
    # get year, month, and day from query params (defaults to current date)
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)
    day = request.GET.get('day', None)  # optional day selection

    try:
        year = int(year)
        month = int(month)
        if day:
            day = int(day)
    except ValueError:
        year = datetime.now().year
        month = datetime.now().month
        day = None

    _, num_days = monthrange(year, month)

    # base query: filter by year and month
    query = Booking.objects.filter(date__year=year, date__month=month)

    # further filter by day if it's selected
    if day:
        query = query.filter(date__day=day)

    # order the bookings by date and user
    bookings = query.order_by('date', 'user__nickname')

    # prepare data for the template
    context = {
        'bookings': bookings,
        'current_year': year,
        'current_month': month,
        'current_day': day,
        'num_days': num_days,
        'months': [  # Month names for dropdown
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        # 1 year backtrack and 5 years ahead, although current logic doesn't allow further than 365days
        'years': range(datetime.now().year - 1, datetime.now().year + 5),
        'days': range(1, num_days + 1)  # Days in the current month
    }

    return render(request, 'all-bookings.html', context)


@login_required
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            print(f"Assigning user {request.user} to booking.")
            booking.user = request.user  # Assign the logged-in user
            try:
                booking.full_clean()  # Run validation after assigning the user
                booking.save()  # Save the booking
                print(f"Booking created for user {booking.user}")
                messages.success(request, "Booking created successfully!")
                return redirect("view_bookings")
            except ValidationError as e:
                form.add_error(None, e.messages)
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = BookingForm()

    return render(request, "create-booking.html", {"form": form})

# @login_required
# def create_booking(request):
#     # Resolve the user explicitly
#     request.user = get_user_model().objects.get(pk=request.user.pk)
#
#     if not request.user.is_authenticated:
#         return HttpResponse("User is not authenticated", status=401)
#
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             print(f"Assigning user {request.user} to booking.")
#             booking.user = request.user  # Set the logged-in user
#             print(f"This is the booking.user {booking.user}")
#             try:
#                 booking.save()
#                 messages.success(request, "Booking created successfully!")
#                 return redirect("view_bookings")
#             except ValidationError as e:
#                 form.add_error(None, e.messages)
#             except Exception as e:
#                 form.add_error(None, str(e))
#     else:
#         form = BookingForm()
#
#
#     from django.utils.encoding import force_str
#
#     resolved_user = force_str(request.user)
#     print(f"Resolved User: {resolved_user}, Type: {type(resolved_user)}")
#
#     if request.user.is_authenticated:
#         print(f"Authenticated User: {request.user}, Type: {type(request.user)}")
#     else:
#         print("User is not authenticated")
#
#     return render(request, "create-booking.html", {"form": form})



@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('date')
    return render(request, "view-bookings.html", {"bookings": bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking deleted successfully!")
    return HttpResponseRedirect(reverse('view_bookings'))


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

            if not phone_number.isdigit() or len(phone_number) != 10:
                return JsonResponse({"error": "Invalid phone number."}, status=400)

            user = request.user
            user.phone_number = phone_number
            user.save()

            return JsonResponse({"phone_number": user.phone_number})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)


""" Debug page for testing login functionalities."""
# def test_login_view(request):
#     # Replace with a valid query for a user
#     user = Account.objects.filter(nickname="tsvtln").first()
#     if not user:
#         return HttpResponse("No user found to log in", status=404)
#     login(request, user)  # Log in the user
#     return HttpResponse(f"User {request.user} is now logged in")


def check_availability(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    try:
        availability = ParkingAvailability.objects.filter(date=date).first()
        if not availability:
            return JsonResponse({'available_spaces': 0})
        return JsonResponse({'available_spaces': availability.available_spaces})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def view_user_profile(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    return render(request, 'user-profile.html', {'user': user})