from .models import Department, Team
from django import forms
from .models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['color', 'progress', 'note'] 
        widgets = {
    'color': forms.RadioSelect(attrs={'class': 'color-radio'}),
    'progress': forms.RadioSelect(attrs={'class': 'progress-radio'}),
    'note': forms.Textarea(attrs={'class': 'comment-box'}),
}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].required = False

        self.fields['color'].required = True
        self.fields['progress'].required = True

        self.fields['color'].choices = [c for c in Vote.COLOR_CHOICES if c[0]]
        self.fields['progress'].choices = [c for c in Vote.PROGRESS_CHOICES if c[0]]

class StartVotingForm(forms.Form):  
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Select Department")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Select Team")
