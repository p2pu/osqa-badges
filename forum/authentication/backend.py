import hashlib

from django.utils.encoding import smart_str

from forum.models import User
from forum.models import lernanta


LERNANTA_DB = 'lernanta_db'


class LernantaAuthBackend:
    """
    Authenticate against existing lernanta user accounts.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        try:
            lernanta_user = lernanta.UserProfile.objects.using(LERNANTA_DB).get(username=username)
        except lernanta.UserProfile.DoesNotExist:
            return None
        try:
            user = User.objects.get(username=lernanta_user.username)
            user.is_active = lernanta_user.user.is_active
            user.save()
        except User.DoesNotExist:
            user = User(username=username)
        if not lernanta_user.user.is_active or not lernanta_user.password:
            return None
        pwd_valid = self.check_password(lernanta_user, user, password)
        if pwd_valid:
            LernantaAuthBackend.get_user_data(lernanta_user, user)
            if User.objects.all().count() == 0:
                user.is_superuser = True
                user.is_staff = True
            user.save()
            return user
        else:
            return None

    def check_password(self, lernanta_user, user, password):
        if '$' not in lernanta_user.password:
            is_correct = (lernanta_user.password == self.get_hexdigest('md5', '', password))
        else:
            algo, salt, hsh = lernanta_user.password.split('$')
            is_correct = (hsh == self.get_hexdigest(algo, salt, password))
        return is_correct

    def get_hexdigest(self, algorithm, salt, raw_password):
        """Generate password hash."""
        return hashlib.new(algorithm, smart_str(salt + raw_password)).hexdigest()

    @classmethod
    def get_user_data(cls, lernanta_user, user):
        user.email = lernanta_user.email
        user.email_isvalid = True
        user.real_name = lernanta_user.full_name
        user.location = lernanta_user.location
        user.about = lernanta_user.bio

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_openid_user(cls, assoc_key):
        try:
            user_openid = lernanta.UserOpenID.objects.using(LERNANTA_DB).get(display_id__exact=assoc_key)
            lernanta_user = lernanta.UserProfile.objects.using(LERNANTA_DB).get(user=user_openid.user)
            try:
                user = User.objects.get(username=lernanta_user.username)
            except User.DoesNotExist:
                user = User(username=lernanta_user.username)
                cls.get_user_data(lernanta_user, user)
                user.save()
            return user
        except lernanta.UserOpenID.DoesNotExist, lernanta.UserProfile.DoesNotExist:
            return None


