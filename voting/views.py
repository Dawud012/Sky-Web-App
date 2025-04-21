from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StartVotingForm, VoteForm
from .models import HealthCard, Session, Team, Vote
from datetime import date

# Function to start the voting process by selecting the team and creating a session
@login_required
def start_voting(request):
    if request.method == "POST":
        form = StartVotingForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            request.session['selected_team_id'] = team.id

            # Create a new session in the database
            session = Session.objects.create(date=date.today(), status='Active')

            # Store the session ID in the session cookie
            request.session['vote_session_id'] = session.id

            # Redirect to the first health card
            first_card = HealthCard.objects.order_by('id').first()
            if first_card:
                return redirect('submit_vote', card_id=first_card.id)
    else:
        form = StartVotingForm()

    return render(request, 'voting/start_voting.html', {'form': form})

# After submitting votes, thank the user
@login_required
def thank_you(request):
    return render(request, 'voting/thank_you.html')

@login_required
def submit_vote(request, card_id):
    # Retrieve session_id and team_id from session data
    session_id = request.session.get('vote_session_id')
    team_id = request.session.get('selected_team_id')

    # Ensure session and team exist in the database
    if not session_id or not team_id:
        return redirect('start_voting')

    # Fetch session and team from the database
    session = get_object_or_404(Session, id=session_id)
    team = get_object_or_404(Team, id=team_id)

    # Get the current health card
    card = get_object_or_404(HealthCard, id=card_id)

    # Get all health cards in order for navigation
    cards = list(HealthCard.objects.order_by('id'))
    current_index = cards.index(card)
    total_cards = len(cards)

    # Check if the user has already voted on this card in the current session
    existing_vote = Vote.objects.filter(user=request.user, card=card, session=session).first()

    # Handle POST request for vote submission
    if request.method == "POST":
        form = VoteForm(request.POST, instance=existing_vote)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.card = card
            vote.session = session  # Link the vote to the current session
            vote.team = team
            vote.save()

            # Navigate to the next card or finalize if it's the last card
            next_card = cards[current_index + 1] if current_index + 1 < total_cards else None
            if next_card:
                return redirect('submit_vote', card_id=next_card.id)
            else:
                # If it’s the last card, clean up the session and redirect to the thank you page
                request.session.pop('vote_session_id', None)
                request.session.pop('selected_team_id', None)
                return redirect('thank_you')
    else:
        form = VoteForm(instance=existing_vote)

    # Provide context for the template (for navigation)
    prev_card_id = cards[current_index - 1].id if current_index > 0 else None
    next_card_id = cards[current_index + 1].id if current_index + 1 < total_cards else None

    return render(request, 'voting/submit_vote.html', {
        'form': form,
        'card': card,
        'current_index': current_index + 1,
        'total_cards': total_cards,
        'prev_card_id': prev_card_id,
        'next_card_id': next_card_id,
    })
