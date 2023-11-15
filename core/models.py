from django.db import models

from django.contrib.auth.models import AbstractUser
from firebase_admin import storage

from firebase_admin import auth 


class Person(AbstractUser):
    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If email is not provided, create a default one based on username
        if not self.email:
            self.email = f"{self.username}@example.com"

        if not self.firebase_uid:
            # Generate a Firebase UID
            firebase_user = auth.create_user(email=self.email, password=self.password)
            self.firebase_uid = firebase_user.uid

        super().save(*args, **kwargs)


