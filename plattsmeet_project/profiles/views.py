from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.conf import settings
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm , SearchForm
#search functionality
from django.contrib.postgres.search import SearchVector
from accounts.views import account_search_view
#Search Functionality

def search_bymajor(request,*args, **kwargs):
    context = {}
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
# """ #view profile
# @login_required
# def view_profile(request):
# 	context = {}
# 	if request.method == 'POST':
# 		profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
# 		if profile_form.is_valid():
# 			context['major'] = profile_form.cleaned_data.get("major")
# 			pronouns= profile_form.cleaned_data.get("pronouns")
# 			hobbies= profile_form.cleaned_data.get("hobbies")
# 			bio=profile_form.cleaned_data.get("bio")
# 	return render(request, 'profiles/viewprofile.html',context)

 
# @login_required
# def profile_search_view(request, *args, **kwargs):
# 	context = {}
# 	if request.method == "GET":
# 		search_query = request.GET.get("q")
# 		if len(search_query) > 0:
# 			#email and username filter
# 			search_results = profile.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
# 			user = request.user
# 			profiles = [] # [(profile1, True), (profile2, False), ...]
# 			for profile in search_results:
# 				profiles.append((profile, False)) # you have no friends yet
# 			context['profiles'] = profiles
				
# 	return render(request, "profile/search.html", context)
# 
# """ @login_required
# def edit_profile(request, *args, **kwargs):
# 	user_id = kwargs.get("user_id")
# 	profile = profile.objects.get(pk=user_id)
# 	if profile.pk != request.user.pk:
# 		return HttpResponse("You cannot edit someone elses profile.")
# 	context = {}
# 	if request.POST:
# 		form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
# 		if form.is_valid():
# 			form.save()
# 			new_username = form.cleaned_data['username']
# 			return redirect("profile:view", user_id=profile.pk)
# 		else:
# 			form = profileUpdateForm(request.POST, instance=request.user,
# 				initial={
# 					"id": profile.pk,
# 					"email": profile.email, 
# 					"username": profile.username,
# 				}
# 			)
# 			context['form'] = form
# 	else:
# 		form = UserUpdateForm(
# 			initial={
# 					"id": profile.pk,
# 					"email": profile.email, 
# 					"username": profile.username,
# 				}
# 			)
# 		context['form'] = form
# 	return render(request, "profile/edit.html", context)



# #request.user.profile
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
# @login_required
# def view_profile(request,*args, **kwargs):
# 	user_id = kwargs.get("user_id")
# 	context ={}
# 	profile =  Profile.objects.get(pk=user_id)
# 	if profile:
# 		context['bio']= profile.bio
# 	return render(request, 'profiles/viewprofile.html')

# """ @login_required
# def update_profile(request):
# 	if request.method == 'POST':
# 		user_form = UserUpdateForm(request.POST, instance=request.user)
# 		if profile_form.is_valid():
# 			profile_form.save()
# 			messages.success(request, ('Your profile was successfully updated!'))
# 			return redirect('portalpage')
# 		else:
# 			messages.error(request, ('Please correct the error below.'))
# 	else:
# 		user_form = UserUpdateForm(request.POST, instance=request.user)
# 		context = {
#         'user_form': user_form,
#     }
# 	return render(request, 'profiles/edit.html', {
# 		  'user_form': user_form,
#     })

#  """ """


#view profile
def profile_view(request):
	return render(request, "profiles/profile.html")

