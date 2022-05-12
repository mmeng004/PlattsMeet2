from django import forms
from profiles.models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required


#Update Profile information
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
         model = Profile
         fields = ['major','firstname','lastname','pronouns','year','hometown','hobbies','bio', 'photo']
    

#Search Form
class SearchForm(forms.Form):
    query = forms.CharField()


