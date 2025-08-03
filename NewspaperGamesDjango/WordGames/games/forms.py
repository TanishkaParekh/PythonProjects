from django import forms

#Scrabble
class PlayerInfo(forms.Form):
    num_players = forms.ChoiceField(
        choices=[(2, '2 Players'), (3, '3 Players'), (4, '4 Players')],
        label="How many players?",
        widget=forms.Select(attrs={'class': 'form-control'}))