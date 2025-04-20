from django.contrib import admin
from .models import Department, Team, UserProfile, HealthCard, Session, Vote

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(HealthCard)
admin.site.register(Session)
admin.site.register(Vote)
