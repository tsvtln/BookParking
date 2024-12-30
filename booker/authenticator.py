import logging

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from booker.models import Account


# logger = logging.getLogger(__name__)

class AccountBackend(BaseBackend):
    def authenticate(self, request, nickname=None, password=None, **kwargs):
        # print(f"Authenticating user with nickname: {nickname}")  # Debugging message
        # logger.debug(f"Authenticating user with nickname: {nickname}")
        try:
            account = Account.objects.get(nickname=nickname)
            # logger.debug(f"Found account: {account}")
            # print(f"Found account: {account}")  # Debugging message
            if check_password(password, account.password):
                # logger.debug("Password is valid.")
                return account
        except Account.DoesNotExist:
            # logger.debug(f"No account found with nickname: {nickname}")
            return None

    def get_user(self, user_id):
        # print(f"Getting user by ID: {user_id}")  # Debugging message
        # logger.debug(f"Getting user by ID: {user_id}")
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            # print("No user found.")  # Debugging message
            # logger.debug(f"No account found with ID: {user_id}")
            return None
