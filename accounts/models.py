# Author :Dawud
# Co-Author : Parham Golmohammadi

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ENGINEER        = 'Engineer'
    TEAM_LEADER     = 'Team Leader'
    DEPT_LEADER     = 'Department Leader'
    SENIOR_MANAGER  = 'Senior Manager'
    ADMIN           = 'Admin'

    ROLE_CHOICES = [
        (ENGINEER,       'Engineer'),
        (TEAM_LEADER,    'Team Leader'),
        (DEPT_LEADER,    'Department Leader'),
        (SENIOR_MANAGER, 'Senior Manager'),
        (ADMIN,          'Admin'),
    ]

    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ENGINEER)
    # These can be ForeignKey to Team if needed, or keep as CharField
    team       = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Create profile when new User is created
    profile, was_created = Profile.objects.get_or_create(user=instance)
    if was_created:
        # Use the constant instead of string
        profile.role = Profile.ENGINEER
        profile.save()