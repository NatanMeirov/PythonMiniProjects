from django.shortcuts import render
from django.http import HttpResponse
from MessageRestApi.models import UserProfile, Message
from MessageRestApi.forms import UserProfileForm, MessageForm, DeleteMessageForm, GetMessagesForm, ReadMessageForm

# Create your views here.


def home(request):
    """A Homepage view, for MANUALLY addition of New Users to the system"""

    new_user_form = UserProfileForm()

    if request.method == "POST":
        new_user_form = UserProfileForm(request.POST)

        if new_user_form.is_valid():
            new_user_form.save()
            return HttpResponse("Successfully Added a New User.")
        else:
            return HttpResponse("An Error has occurred. Could not add the User to the system. (Probable reason: Wrong input).")

    return render(request, "MessageRestApi/Homepage.html", {"new_user_form": new_user_form})


def write_message(request):
    """A Write New Message view, to send a new Message (will be stored in the Database)"""

    message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message_form.save()
            return HttpResponse("Successfully sent the Message.")
        else:
            return HttpResponse("An Error has occurred. Could not send the new Message. (Probable reason: Wrong input).")

    return render(request, "MessageRestApi/WriteMessage.html", {"message_form": message_form})


def delete_message(request):
    """A Delete Message view, to delete one specific Message (from the Database) [identifiers: Username (Owner or Receiver), and Subject]"""

    delete_message_form = DeleteMessageForm()

    if request.method == "POST":
        delete_message_form = DeleteMessageForm(request.POST)

        if delete_message_form.is_valid():
            try:
                user_choice_sender_or_receiver = delete_message_form.clean_validation_and_get_sender_or_receiver()
            except:
                return HttpResponse("Must select only one option to Delete a Message. (Select only one option: Sender or Receiver)")

            username_of_message = delete_message_form.cleaned_data.get("username")
            subject_of_message = delete_message_form.cleaned_data.get("subject")

            try:
                if user_choice_sender_or_receiver == "sender":
                    message_to_delete = Message.objects.get(sender__username = username_of_message, subject = subject_of_message)
                elif user_choice_sender_or_receiver == "receiver": # To be clear
                    message_to_delete = Message.objects.get(receiver__username = username_of_message, subject = subject_of_message)

                message_to_delete.delete()
            except:
                return HttpResponse("An Error has occurred. Could not find the Message in the system. (Probable reason: Wrong input).")

            return HttpResponse("Successfully deleted the Message.")
        else:
            return HttpResponse("An Error has occurred. (Probable reason: Wrong input).")

    return render(request, "MessageRestApi/DeleteMessage.html", {"delete_message_form": delete_message_form})


def get_messages_of_user(request):
    """A Get Messages view, to show all the Messages for a specific User (from the Database). [Can choose to see only the Unread Messages]"""

    get_messages_form = GetMessagesForm()

    if request.method == "POST":
        get_messages_form = GetMessagesForm(request.POST)

        if get_messages_form.is_valid():
            user = get_messages_form.cleaned_data.get("username")

            if get_messages_form.cleaned_data.get("only_unread_messages"): # Wanted Only Unread Messages From The User (only_unread_messages == True)
                messages_as_sender = Message.objects.filter(sender__username = user, already_read = False)
                messages_as_receiver = Message.objects.filter(receiver__username = user, already_read = False)

            else: # (only_unread_messages == False)
                messages_as_sender = Message.objects.filter(sender__username = user)
                messages_as_receiver = Message.objects.filter(receiver__username = user)

            messages_to_display = messages_as_sender | messages_as_receiver # Merging the QuerySets (mame model: Message)
            return render(request, "MessageRestApi/DisplayAllWanedMessages.html", {"messages_to_display": messages_to_display})
        else:
            return HttpResponse("An Error has occurred. (Probable reason: Wrong input).")

    return render(request, "MessageRestApi/GetMessages.html", {"get_messages_form": get_messages_form})


def read_message(request):
    """A Read one Message view, to show the user a specific Message (from the Database). [identifiers: Username (MUST be the Receiver!), and Subject]"""

    read_message_form = ReadMessageForm()

    if request.method == "POST":
        read_message_form = ReadMessageForm(request.POST)

        if read_message_form.is_valid():
            owner_of_message = read_message_form.cleaned_data.get("username")
            subject_of_message = read_message_form.cleaned_data.get("subject")

            try:
                message = Message.objects.filter(receiver__username = owner_of_message, subject = subject_of_message)[0]
            except:
                return HttpResponse("An Error has occurred. (Probable reason: Wrong input - There is not such Message for the User).")

            message.already_read = True
            message.save()

            return render(request, "MessageRestApi/ReadSelectedMessage.html", {"message": message})
        else:
            return HttpResponse("An Error has occurred. (Probable reason: Wrong input).")


    return render(request, "MessageRestApi/ReadMessage.html", {"read_message_form": read_message_form})


def index(request):
    """An Index view, helps to know how to use the system"""

    return render(request, "MessageRestApi/Index.html")





