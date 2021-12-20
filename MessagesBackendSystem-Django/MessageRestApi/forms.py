from django import forms
from django.db import models
from django.core import validators
from MessageRestApi.models import UserProfile, Message

def check_for_existing_user(value):
    """A custom validator to check if the User info is correct."""

    name_of_user_for_check = str(value) # In case of a Message's sender and receiver UserProfile instance - taking a string presentation

    if not UserProfile.objects.filter(username = name_of_user_for_check).exists():
        raise validators.ValidationError("The User doesn't exists...")

    return True



class UserProfileForm(forms.ModelForm):
    """Form definition for the creation of new UserProfile in the system."""
    username = forms.CharField(label = "Username", validators = [validators.MinLengthValidator(0)])
    password = forms.CharField(label = "Password", widget = forms.PasswordInput, validators = [validators.MinLengthValidator(0)])

    class Meta:
        """Meta definition for UserProfileForm."""

        model = UserProfile
        fields = "__all__"


class MessageForm(forms.ModelForm):
    """Form definition for new Messages in the system."""

    sender = forms.ModelChoiceField(queryset = models.QuerySet(UserProfile), to_field_name = "username", label = "From")
    receiver = forms.ModelChoiceField(queryset = models.QuerySet(UserProfile), to_field_name = "username", label = "To")
    subject = forms.CharField(label = "Subject", validators = [validators.MinLengthValidator(0)])
    message = forms.CharField(label = "Message", widget = forms.Textarea, validators = [validators.MinLengthValidator(0)])

    class Meta:
        """Meta definition for MessageForm."""

        model = Message
        exclude = ["creation_date", "already_read"]


class DeleteMessageForm(forms.Form):
    """DeleteMessageForm definition."""

    username = forms.CharField(label = "Enter your Username (Owner or Reciever only!)", validators = [check_for_existing_user])
    subject = forms.CharField(label = "Enter the Subject of the Message", validators = [validators.MinLengthValidator(0)])
    as_sender = forms.BooleanField(initial = False, widget = forms.CheckboxInput, label = "As a Sender?", required = False) # initial (in regular Form) is equal to default (in ModelForm)
    as_receiver = forms.BooleanField(initial = False, widget = forms.CheckboxInput, label = "As a Receiver?", required = False)

    def clean_validation_and_get_sender_or_receiver(self):
        """Clean method to check if the input from the User is correct"""
        user_choice_as_sender = self.cleaned_data.get("as_sender")
        user_choice_as_receiver = self.cleaned_data.get("as_receiver")

        if user_choice_as_sender == user_choice_as_receiver:
            raise forms.ValidationError("Must select only one option!")

        if user_choice_as_sender:
            return "sender"

        if user_choice_as_receiver:
            return "receiver"


class GetMessagesForm(forms.Form):
    """GetMessagesForm definition."""

    username = forms.CharField(label = "Enter your Username", validators = [check_for_existing_user])
    only_unread_messages = forms.BooleanField(initial = False, label = "Only Unread Messages", required = False)

class ReadMessageForm(forms.Form):
    """ReadMessageForm definition."""

    username = forms.CharField(label = "Enter your Username (Receiver)", validators = [check_for_existing_user])
    subject = forms.CharField(label = "Enter the Subject of the Message", validators = [validators.MinLengthValidator(0)])








