from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    """
    Allow authentication using either username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get("email")

        if username is None or password is None:
            return None

        try:
            # Try email first
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            try:
                # Then try username
                user = UserModel.objects.get(username__iexact=username)
            except UserModel.DoesNotExist:
                # Prevent timing attacks
                UserModel().set_password(password)
                return None

        # Use Django's built-in authentication logic
        if user.check_password(password) and user.is_active:
            return user

        return None