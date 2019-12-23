from django.conf import settings
from django.contrib.auth.hashers import check_password
from accounts.models import User

print('backend.py runs')

class MyBackend(object):
    def authenticate(self, request, username=None, password=None):
        print('Custom authentication initialised.')
        try:
            print('Trying to find the user now.')
            user = User.objects.get(email=username)
        except User.MultipleObjectsReturned:
            print('More than one user with email : {}'.format(email))
            return None
        except User.DoesNotExist:
            print('User Does not Exists.')
            return None
        # print('backend')

        if user.is_active and user.check_password(password):
            print('Authentivation completed succesfully.')
            return user
        print('Authentivation went wrong on backend.py')
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
