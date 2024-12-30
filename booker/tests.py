# from django.test import TestCase
#
# # Create your tests here.
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkingBooker.settings')  # Replace with your settings module
django.setup()
#
# from django.contrib.auth import authenticate
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkingBooker.settings')
# django.setup()
#
# # Test authentication
# user = authenticate(username='nickname_here', password='correct_password')
# if user:
#     print(f"User authenticated: {user}")
# else:
#     print("Invalid username or password!")
#
#
#
# from booker.models import Account
# from django.contrib.auth.hashers import check_password
#
# nickname = 'your_nickname_here'  # Replace with the nickname
# password = 'your_correct_password_here'  # Replace with the correct password
#
# # Retrieve the account
# try:
#     account = Account.objects.get(nickname=nickname)
#     print(f"Account found: {account}")
#
#     # Verify the password
#     password_valid = check_password(password, account.password)
#     print(f"Password valid: {password_valid}")
# except Account.DoesNotExist:
#     print("Account does not exist.")
