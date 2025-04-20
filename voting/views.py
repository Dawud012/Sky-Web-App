from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VoteForm
from .models import Vote, HealthCard, Team
from .forms import StartVotingForm


def start_voting(request):
    """
    User selects department and team.
    Stores it in session and redirects to first vote card.
    """
    if request.method == "POST":
        form = StartVotingForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            request.session['selected_team_id'] = team.id
            first_card = HealthCard.objects.order_by('id').first()
            if first_card:
                return redirect('submit_vote', card_id=first_card.id)
    else:
        form = StartVotingForm()

    return render(request, 'voting/start_voting.html', {'form': form})


@login_required
def submit_vote(request, card_id):
    """
    Handles submission of a vote for a specific health card.
    Displays a form for one card at a time, moves to the next one after submission.
    """

    card = get_object_or_404(HealthCard, id=card_id)
    cards = list(HealthCard.objects.order_by('id'))
    current_index = cards.index(card)
    total_cards = len(cards)

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.card = card

            # Use the selected team from session, or fallback to profile
            team_id = request.session.get('selected_team_id')
            if team_id:
                vote.team = get_object_or_404(Team, id=team_id)
            else:
                vote.team = request.user.userprofile.team

            vote.session_id = 1  # assuming 1 is the current session
            vote.save()

            # Redirect to next health card or summary
            next_card = HealthCard.objects.filter(id__gt=card.id).order_by('id').first()
            if next_card:
                return redirect('submit_vote', card_id=next_card.id)
            else:
                return redirect('start_voting')
    else:
        # GET request - display form with current card
        form = VoteForm(initial={'card': card})

    return render(request, 'voting/submit_vote.html', {
    'form': form,
    'card': card,
    'current_index': current_index + 1,  # for human-readable display
    'total_cards': total_cards,
    'prev_card_id': cards[current_index - 1].id if current_index > 0 else None,
    'next_card_id': cards[current_index + 1].id if current_index < total_cards - 1 else None,
})
