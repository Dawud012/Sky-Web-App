from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VoteForm, StartVotingForm
from .models import Vote, HealthCard, Team

def start_voting(request):
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
    card = get_object_or_404(HealthCard, id=card_id)
    cards = list(HealthCard.objects.order_by('id'))
    current_index = cards.index(card)
    total_cards = len(cards)

    session_id = 1 

    # Try to fetch an existing vote for this user/card/session
    existing_vote = Vote.objects.filter(user=request.user, card=card, session_id=session_id).first()

    if request.method == "POST":
        form = VoteForm(request.POST, instance=existing_vote)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.card = card
            vote.session_id = session_id

            team_id = request.session.get('selected_team_id')
            vote.team = get_object_or_404(Team, id=team_id) if team_id else request.user.userprofile.team

            vote.save()

            # Get the next card (higher ID)
            next_card = HealthCard.objects.filter(id__gt=card.id).order_by('id').first()
            if next_card:
                return redirect('submit_vote', card_id=next_card.id)
            else:
                return redirect('start_voting')  # or redirect to a thank you page
    else:
        # If GET, show form prefilled with existing vote or blank
        form = VoteForm(instance=existing_vote, initial={'card': card})

    return render(request, 'voting/submit_vote.html', {
        'form': form,
        'card': card,
        'current_index': current_index + 1,
        'total_cards': total_cards,
        'prev_card_id': cards[current_index - 1].id if current_index > 0 else None,
        'next_card_id': cards[current_index + 1].id if current_index < total_cards - 1 else None,
    })



