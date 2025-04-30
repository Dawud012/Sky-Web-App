# Author : Parham Golmohammadi
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StartVotingForm, VoteForm
from .models import HealthCard, Session, Team, Vote
from datetime import date
from accounts.decorators import restrict_to_roles
from accounts.models import Profile


# First step in voting: user picks a team, and we create a new session
@login_required
@restrict_to_roles(Profile.ENGINEER, Profile.TEAM_LEADER)
def start_voting(request):
    if request.method == "POST":
        form = StartVotingForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            department = team.department  

            profile = request.user.profile
            profile.team = team.name  
            profile.department = department.name  
            profile.save()

            request.session['selected_team_id'] = team.id
            session = Session.objects.create(date=date.today(), status='Active')
            request.session['vote_session_id'] = session.id

            first_card = HealthCard.objects.order_by('id').first()
            if first_card:
                return redirect('tutorial')
            else:
                return redirect('start_voting')
        else:
            # Form is invalid: try to prepopulate the department
            team_id = request.POST.get('team')
            if team_id:
                try:
                    team = Team.objects.get(id=team_id)
                    form.fields['department'].initial = team.department
                except Team.DoesNotExist:
                    pass
    else:
        form = StartVotingForm()


    return render(request, 'voting/start_voting.html', {'form': form})




# Handles the actual voting for each health card
@login_required
@restrict_to_roles(Profile.ENGINEER, Profile.TEAM_LEADER)
def submit_vote(request, card_id):
    # get session and team IDs from the browser session
    session_id = request.session.get('vote_session_id')
    team_id = request.session.get('selected_team_id')

    # if user somehow skipped the start step, send them back
    if not session_id or not team_id:
        return redirect('start_voting')

    # load session and team from the DB
    session = get_object_or_404(Session, id=session_id)
    team = get_object_or_404(Team, id=team_id)

    # get the card we're currently voting on
    card = get_object_or_404(HealthCard, id=card_id)

    # get all cards to manage navigation
    cards = list(HealthCard.objects.order_by('id'))
    current_index = cards.index(card)
    total_cards = len(cards)

    # check if user already voted on this card
    existing_vote = Vote.objects.filter(user=request.user, card=card, session=session).first()

    if request.method == "POST":
        form = VoteForm(request.POST, instance=existing_vote)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.card = card
            vote.session = session
            vote.team = team
            vote.save()

            # decide whether to go to next card or finish voting
            next_card = cards[current_index + 1] if current_index + 1 < total_cards else None
            if next_card:
                return redirect('submit_vote', card_id=next_card.id)
            else:
                # voting is done — mark session as closed 
                session.status = 'Closed'
                session.save()
                request.session.pop('vote_session_id', None)
                request.session.pop('selected_team_id', None)
                return redirect('thank_you')
    else:
        form = VoteForm(instance=existing_vote)

    # passed to template for rendering form and nav buttons
    prev_card_id = cards[current_index - 1].id if current_index > 0 else None
    next_card_id = cards[current_index + 1].id if current_index + 1 < total_cards else None

    progress_percentage = int(((current_index + 1) / total_cards) * 100)

    return render(request, 'voting/submit_vote.html', {
    'form': form,
    'card': card,
    'current_index': current_index + 1,
    'total_cards': total_cards,
    'prev_card_id': prev_card_id,
    'next_card_id': next_card_id,
    'progress_percentage': progress_percentage, 
})

# Author : Aleena
# Tutorial (after choosing team)
@login_required
@restrict_to_roles(Profile.ENGINEER, Profile.TEAM_LEADER)
def tutorial_view(request):
    if request.method == "POST":
        first = HealthCard.objects.order_by('id').first()
        return redirect('submit_vote', card_id=first.id) if first else redirect('start_voting')
    return render(request, 'voting/tutorial.html')




# After a user finishes voting, show them a simple thank you page
@login_required
@restrict_to_roles(Profile.ENGINEER, Profile.TEAM_LEADER)
def thank_you(request):
    return render(request, 'voting/thank_you.html')


