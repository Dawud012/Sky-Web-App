from django.shortcuts import render, get_object_or_404
from voting.models import Vote, HealthCard
from django.contrib.auth.decorators import login_required
from accounts.decorators import restrict_to_roles
from accounts.models import Profile

@login_required
@restrict_to_roles(Profile.TEAM_LEADER, Profile.DEPT_LEADER, Profile.SENIOR_MANAGER)
def trends_page(request):
    cards = HealthCard.objects.all()
    return render(request, 'trends/trends.html', {'cards': cards})

@login_required
@restrict_to_roles(Profile.TEAM_LEADER, Profile.DEPT_LEADER, Profile.SENIOR_MANAGER)
def topic_trends_view(request, topic_id):
    card = get_object_or_404(HealthCard, id=topic_id)
    votes = Vote.objects.filter(card=card)

    green = votes.filter(color='Green').count()
    yellow = votes.filter(color='Yellow').count()
    red = votes.filter(color='Red').count()

    improving = votes.filter(progress='Improving').count()
    stable = votes.filter(progress='Stable').count()
    declining = votes.filter(progress='Declining').count()

    comments = votes.exclude(note="").values_list('note', flat=True)

    context = {
        'card': card,
        'green': green,
        'yellow': yellow,
        'red': red,
        'improving': improving,
        'stable': stable,
        'declining': declining,
        'comments': comments
    }

    return render(request, 'trends/topic_trend_detail.html', context)
