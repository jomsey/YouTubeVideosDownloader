from django import forms

class UserInputForm(forms.Form):
    query = forms.CharField(label="Video Url" ,required=True, widget=forms.TextInput(attrs={"placeholder":"Search Video Or Enter Video Url"}))

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200,required=True)