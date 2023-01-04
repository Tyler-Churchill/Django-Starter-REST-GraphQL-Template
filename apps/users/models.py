from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class User(AbstractUser):
    name = CharField(max_length=512)
