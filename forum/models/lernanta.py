# This is an auto-generated Django model module.
from django.db import models


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=90)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'


class UserOpenID(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    claimed_id = models.TextField()
    display_id = models.TextField()
    class Meta:
        db_table = u'django_openid_auth_useropenid'


class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=765)
    password = models.CharField(max_length=765)
    email = models.CharField(unique=True, max_length=225, blank=True)
    bio = models.TextField()
    confirmation_code = models.CharField(max_length=765)
    location = models.CharField(max_length=765)
    created_on = models.DateTimeField()
    user = models.ForeignKey(AuthUser, null=True, blank=True)
    image = models.CharField(max_length=300, blank=True)
    featured = models.IntegerField()
    newsletter = models.IntegerField()
    discard_welcome = models.IntegerField()
    full_name = models.CharField(max_length=765, blank=True)
    preflang = models.CharField(max_length=48)
    deleted = models.IntegerField()
    class Meta:
        db_table = u'users_userprofile'

