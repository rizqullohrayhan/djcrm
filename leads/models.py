import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver


class User(AbstractUser):
    """
        password
        last_login
        is_superuser
        username
        first_name
        last_name
        email
        is_staff
        is_active
        date_joined
        groups
        user_permissions
    """
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    

class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)


@receiver(pre_save, sender=Lead)
def delete_old_file(sender, instance, **kwargs):
    if not instance.pk:
        return   # Jika instance baru, tidak perlu menghapus file lama.

    try:
        old_file = sender.objects.get(pk=instance.pk).profile_picture
    except sender.DoesNotExist:
        return  # Jika tidak ada instance lama, tidak perlu menghapus file.

    # Hapus file lama jika berbeda dengan file baru
    new_file = instance.profile_picture
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=Lead)
def delete_file_on_delete(sender, instance, **kwargs):
    file = instance.profile_picture
    if file and os.path.isfile(file.path):
        os.remove(file.path)
