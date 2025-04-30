# Author : Parham Golmohammadi

from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile  # Import Profile from accounts


# Department & Team models - these can stay in voting app
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Represents a department in the company.

class Team(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

# Represents a team that belongs to a department.


# Health Check System

class HealthCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
# Health cards represent criteria to vote on.

class Session(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]

# A session is a voting period for team health checks.
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.date} - {self.status}"


class Vote(models.Model):
    COLOR_CHOICES = [
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Red', 'Red'),
    ]

    PROGRESS_CHOICES = [
        ('Improving', 'Improving'),
        ('Stable', 'Stable'),
        ('Declining', 'Declining'),
    ]

    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    progress = models.CharField(max_length=15, choices=PROGRESS_CHOICES)
    note = models.TextField(blank=True)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'card', 'session')

    def __str__(self):
        return f"{self.user.username} - {self.card.name} - {self.color}"