from django.contrib.auth.models import User
from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
#     bio = models.TextField(blank=True)  # 个人简介
#     personal_experience = models.TextField(blank=True)  # 个人经历
#     skills = models.TextField(blank=True)  # 技能

#     def __str__(self):
#         return f"{self.user.username}'s Profile"
