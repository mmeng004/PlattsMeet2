from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.conf import settings
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm
from .forms import SearchForm
from accounts.views import account_view
#search functionality
from django.contrib.postgres.search import SearchVector
#search functionality

@login_required
#Search Functionality - major
def search_bymajor(request,*args, **kwargs):
	form = SearchForm()
	query = None 
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Profile.objects.annotate(
				search=SearchVector('major'),
				).filter(search=query)
	return render(request,
				'profiles/searchbymajor.html',
				{'form': form,
				'query': query,
				'results': results})
    
@login_required
#search view - hobbies
def search_byhobbies(request):
     form = SearchForm()
     query = None
     results = []

     if 'query' in request.GET:
         form = SearchForm(request.GET)
         if form.is_valid():
             query = form.cleaned_data['query']
             results = Profile.objects.annotate(
                 search=SearchVector('hobbies'),
            ).filter(search=query)
     return render(request,
                   'profiles/searchbyhobbies.html',
                    {'form': form,
                    'query': query,
                    'results': results})
@login_required
#search view - hobbies
def search_byhometown(request):
     form = SearchForm()
     query = None
     results = []

     if 'query' in request.GET:
         form = SearchForm(request.GET)
         if form.is_valid():
             query = form.cleaned_data['query']
             results = Profile.objects.annotate(
                 search=SearchVector('hometown'),
            ).filter(search=query)
     return render(request,
                   'profiles/searchbyhometown.html',
                    {'form': form,
                    'query': query,
                    'results': results})


@login_required
def update_profile(request):
 	if request.method == 'POST':
 		profile_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.user_profile)
 		if profile_form.is_valid():
 			profile_form.save()
 			messages.success(request, 'Your profile was successfully updated!')
 			return redirect('profile:viewprofile')
 		else:
 			messages.error(request, 'Please correct the error below.')
 	else:
 		profile_form = ProfileUpdateForm(instance=request.user.user_profile)
 		context = {
        'profile_form': profile_form,
     }
 	return render(request, 'profiles/createprofile.html', {
 		 'profile_form': profile_form,
     })


#view profile
def profile_view(request):
	return render(request, "profiles/profile.html")
