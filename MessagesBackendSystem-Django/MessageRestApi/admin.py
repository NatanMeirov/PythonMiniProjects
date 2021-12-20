from django.contrib import admin

# Register your models here.

from MessageRestApi.models import UserProfile, Message

admin.site.register(UserProfile)
admin.site.register(Message)

# Admin Interface Super User Information:
# Username: NatanMeirov
# Email: NatanMeirov@gmail.com
# Password: Meirov300519

