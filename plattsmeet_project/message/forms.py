#Based on the tutorial from https://www.youtube.com/watch?v=oxrQdZ5KqW0 
from django import forms
class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'myInputClass'}))
class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000, widget=forms.Textarea(attrs={'class': 'myAreaClass'}))