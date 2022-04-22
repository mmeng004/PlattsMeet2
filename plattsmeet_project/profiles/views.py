from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.conf import settings
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from.models import Profile


#request.user.profile
@login_required
def update_profile(request):
	if request.method == 'POST':
		profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('portalpage')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		profile_form = ProfileUpdateForm(instance=request.user.profile)
		context = {
        'profile_form': profile_form
    }
	return render(request, 'profiles/createprofile.html', {
		 'profile_form': profile_form
    })
	
@login_required
def view_profile(request,*args, **kwargs):
	user_id = kwargs.get("user_id")
	context ={}
	profile =  Profile.objects.get(pk=user_id)
	if profile:
		context['bio']= profile.bio
	return render(request, 'profiles/viewprofile.html')

""" @login_required
def update_account(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		if account_form.is_valid():
			account_form.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('portalpage')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		user_form = UserUpdateForm(request.POST, instance=request.user)
		context = {
        'user_form': user_form,
    }
	return render(request, 'profiles/edit.html', {
		  'user_form': user_form,
    })

 """
