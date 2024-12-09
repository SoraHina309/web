from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    Image = models.ImageField()
    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"contact info ({self.email})"


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    @classmethod
    def get_or_create(cls, user):
        profile, created = cls.objects.get_or_create(user=user)
        if created:
            print(f"Created profile for {user.username}")
        return profile
    
class Image(models.Model):
    name = models.CharField(max_length=255)
    image_path = models.ImageField(upload_to='images/')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# Create your models here.
