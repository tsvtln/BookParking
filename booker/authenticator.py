from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from booker.models import Account


class AccountBackend(BaseBackend):
    """
     Authentication service. Currently, we have the authenticator locally, it's authenticating with nickname.
     Alternatively if possible an SSO integration can be related, so the authentication happens on pronet side,
     with pronet credentials.
     We also obfuscate the password by hashing.
    """
    def authenticate(self, request, nickname=None, password=None, **kwargs):
        try:
            account = Account.objects.get(nickname=nickname)
            if check_password(password, account.password):
                return account
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        # We get the user by id
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
