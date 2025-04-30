# Author : Parham Golmohammadi

from .models import Department, Team, Vote
from django import forms


# form used for voting on a single card
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['color', 'progress', 'note']  # note is optional, others are required
        widgets = {
            'color': forms.RadioSelect(attrs={'class': 'color-radio'}),
            'progress': forms.RadioSelect(attrs={'class': 'progress-radio'}),
            'note': forms.Textarea(attrs={'class': 'comment-box'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # note is optional, others are required
        self.fields['note'].required = False
        self.fields['color'].required = True
        self.fields['progress'].required = True

        # use only non-empty choices (just in case)
        self.fields['color'].choices = [c for c in Vote.COLOR_CHOICES if c[0]]
        self.fields['progress'].choices = [c for c in Vote.PROGRESS_CHOICES if c[0]]


# this is the first step form where user picks their team + department
class StartVotingForm(forms.Form):  
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Select Department",
        required=False 
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Select Team"
    )
