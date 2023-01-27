from django import forms


class SearchForm(forms.Form):
    id_kinopoisk = forms.CharField(max_length=200, required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter title film'}))
