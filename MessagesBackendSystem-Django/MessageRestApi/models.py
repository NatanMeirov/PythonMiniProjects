from django.db import models


# Create your models here.


class UserProfile(models.Model):
    """Database model for users in the system."""
    username = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique = True)

    def __str__(self):
        return self.username


class Message(models.Model):
    """Database model for messages in the system."""
    # sender and receiver - Many-to-one relationships:
    sender = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "receiver")
    creation_date = models.DateTimeField(auto_now_add = True) # Saving the Date and the Time of the first creation of the message
    subject = models.CharField(max_length = 255)
    message = models.TextField()
    already_read = models.BooleanField(default = False)

    def __str__(self):
        return f"Message From: {self.sender} To {self.receiver}, Subject: {self.subject}, Date: {self.creation_date}"





# AUTH_USER (not fully implemented):
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# class UserProfile(AbstractBaseUser, PermissionsMixin):
#     """
#     [summary]
#     Database model for users in the system
#     """
#     username = models.CharField(max_length = 255, unique = True)
#     password = models.CharField(max_length = 255)
#     email = models.EmailField(max_length = 255, unique = True)
#     is_active = models.BooleanField(default = True)

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]

#     def get_full_name(self):
#         """
#         [summary]
#         Retrieve full name of user
#         """
#         return self.username

#     def get_short_name(self):
#         """
#         [summary]
#         Retrieve short name of user
#         """
#         return self.username

#     def __str__(self):
#         return f"{self.username}: {self.email}"

