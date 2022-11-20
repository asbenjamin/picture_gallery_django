from django.contrib.auth.models import BaseUserManager, User
from django.db import models
from rest_framework.authtoken.models import Token


class Photo(models.Model):
    image = models.FileField(upload_to="images")
    title = models.CharField(blank=True, null=True, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    image_url = models.URLField(blank=True, null=True, max_length=255)
    owner = models.ForeignKey(User, related_name="photos", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title + ": " + self.image_url


class MyUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **kwargs):
        """
        Creates and saves a User with the given email, phone
        number and password.
        """

        user = self.model(username=username, **kwargs)
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        # Create a token for this user
        Token.objects.get_or_create(user=user)
        return user
