from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from booker.models import Account


class AccountBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = Account.objects.get(nickname=username)
            if check_password(password, account.password):
                return account
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
