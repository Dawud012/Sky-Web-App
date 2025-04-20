from .models import Department, Team
from django import forms
from .models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['card', 'color', 'progress', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].required = False

class StartVotingForm(forms.Form):  # ✅ match import
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Select Department")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Select Team")
