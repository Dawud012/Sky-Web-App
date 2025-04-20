from django.shortcuts import render, redirect
from .forms import VoteForm
from .models import Vote

def submit_vote(request):
    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user  # current logged in user
            vote.team = request.user.userprofile.team  # from profile
            vote.save()
            return redirect('vote_summary')
    else:
        form = VoteForm()
    return render(request, 'voting/submit_vote.html', {'form': form})

def vote_summary(request):
    votes = Vote.objects.all()
    return render(request, 'voting/vote_summary.html', {'votes': votes})
