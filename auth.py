from django.contrib.auth.models import User
from django.db import connection

users = User.objects.all()
print("Users:", [user.username for user in users])

print("Using database:", connection.settings_dict['NAME'])