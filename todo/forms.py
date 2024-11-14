from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={'placeholder': 'Title',
                                                          'class': 'form-control',
                                                          'type': 'text',
                                                          'required': 'required',
                                                          'data-validation-required-message': 'Please enter name film.'}))
