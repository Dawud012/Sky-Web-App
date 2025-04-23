from django.db import models
from django.contrib.auth.models import User
from datetime import date

# team and department setup
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department.name})"


# user roles and profile
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Engineer', 'Engineer'),
        ('Team Leader', 'Team Leader'),
        ('Department Leader', 'Department Leader'),
        ('Senior Manager', 'Senior Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# models for health checks and team voting process
class HealthCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Session(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]

    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        # auto-close sessions if the date is already past
        if self.date < date.today() and self.status == 'Active':
            self.status = 'Closed'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.status}"


# user responses to health cards
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
    note = models.TextField(blank=True)  # optional: user can leave feedback
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'card', 'session_id')  # prevent duplicate votes per user/card/session

    def __str__(self):
        return f"{self.user.username} - {self.card.name} - {self.color}"
