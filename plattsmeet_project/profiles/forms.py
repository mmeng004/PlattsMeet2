from django import forms
from profiles.models import Profile

 #Update Profile information
class ProfileUpdateForm(forms.ModelForm):
     class Meta:
         model = Profile
         fields = ['major','pronouns','hobbies','bio', 'photo']


