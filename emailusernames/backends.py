from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from emailusernames.utils import get_user, get_user_custom_model_name


class EmailAuthBackend(ModelBackend):

    """Allow users to log in with their email address"""

    def authenticate(self, email=None, password=None, **kwargs):
        # Some authenticators expect to authenticate by 'username'
        if email is None:
            email = kwargs.get('username')

        try:
            user = get_user(email)
            if user.check_password(password):
                user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_user_custom_model_name()
        return self._user_class
