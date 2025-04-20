from django.db import models
from django.contrib.auth.models import User

#model creation

class HealthCard(models.Model):
    card_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.card_name
    
class Session(models.Model):
    session_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Closed', 'Closed')])

    def __str__(self):
        return f"{self.session_date} - {self.status}"


class Vote(models.Model):
    COLOR_CHOICES = [
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Red', 'Red')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=COLOR_CHOICES)
    note = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.card.card_name} - {self.vote}"