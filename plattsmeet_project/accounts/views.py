# from django.http import HttpResponse
# from django.shortcuts import render
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Profile
# from .forms import LoginForm, UserRegistrationForm, UserEditForm,ProfileEditForm
# from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from accounts.models import Account 
from django.contrib.auth import login, authenticate, logout
from accounts.forms import UserLoginForm, RegistrationForm,UserUpdateForm 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from friend.utils import get_friend_request_or_false
from friend.request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from profiles.models import Profile



#works register view
def register(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			# Create the user profile
			#Profile.objects.create(user = new_user)
            #register and login
			email = form.cleaned_data.get('email').lower()
			password = form.cleaned_data.get('password1') 
			account = authenticate(email=email, password=password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

#works logout view
def logoutview(request):
	logout(request)
	return redirect("home")

	
#works login view
def userlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['email'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("portalpage")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(
#                 user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # Create the user profile
#             Profile.objects.create(user=new_user)
#             return render(request,
#                           'account/register_done.html',
#                           {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,
#                   'account/register.html',
#                   {'user_form': user_form})

# @login_required
# """ # def edit(request):
#       if request.method == 'POST':
#           user_form = UserEditForm(instance=request.user,
#                                    data=request.POST)
#           profile_form = ProfileEditForm(
#                                       instance=request.user.profile,
#                                       data=request.POST,
#                                       files=request.FILES)
#           if user_form.is_valid() and profile_form.is_valid():
#               user_form.save()
#               profile_form.save()
#              messages.success(request, 'Profile updated successfully')
#           else:
#               messages.error(request, 'Error updating your profile')
#       else:
#           user_form = UserEditForm(instance=request.user)
#           profile_form = ProfileEditForm(instance=request.user.profile)
#       return render(request,
#                     'account/edit.html',
#                     {'user_form': user_form,
#                     'profile_form': profile_form})


#view account view
def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self
		is_friend
			-1: NO_REQUEST_SENT
			0: THEM_SENT_TO_YOU
			1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
		profile = Profile.objects.get(user=user_id)
	except:
		return HttpResponse("User does not exist .")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['hide_email'] = account.hide_email
		context['firstname'] = profile.firstname
		context['lastname'] = profile.lastname
		context['major'] = profile.major
		context['year'] = profile.year
		context['pronouns'] = profile.pronouns
		context['hobbies'] = profile.hobbies
		context['bio'] = profile.bio
		context['photo'] = profile.photo
		

		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends
	
		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html", context)


# """ def update_account(request):
# 	if request.method == 'POST':
# 		user_form = UserUpdateForm(request.POST, instance=request.user)
# 		if user_form.is_valid():
# 			user_form.save()
# 			messages.success(request, ('Your profile was successfully updated!'))
# 			return redirect('portalpage')
# 		else:
# 			messages.error(request, ('Please correct the error below.'))
# 	else:
# 		user_form = UserUpdateForm(request.POST, instance=request.user)
# 		context = {
#         'user_form': user_form,
#     }
# 	return render(request, 'accounts/edit.html', {
# 		  'user_form': user_form,
#     }) """


#works search accounts
@login_required
def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			#email and username filter
			search_results = Account.objects.filter(username__icontains=search_query).distinct()
			#psearch_results = Profile.objects.filter(firstname__icontains=search_query).filter(lastname__icontains=search_query).distinct()
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "account/search.html", context)



#works account edit 
@login_required
def edit_account(request, *args, **kwargs):
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses account.")
	context = {}
	if request.POST:
		form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile was successfully updated!')
			new_username = form.cleaned_data['username']
			return redirect("account:view", user_id=account.pk)
		else:
			messages.error(request, 'Please correct the error below.')
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
				}
			)
			context['form'] = form
	else:
		form = UserUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
				}
			)
		context['form'] = form
	return render(request, "account/edit.html", context)





# """ @login_required
# def update_profile(request):
# 	if request.method == 'POST':
# 		user_form = UserUpdateForm(request.POST, instance=request.user)
# 		profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			user_form.save()
# 			profile_form.save()
# 			messages.success(request, _('Your profile was successfully updated!'))
# 			return redirect('portalpage')
# 		else:
# 				messages.error(request, _('Please correct the error below.'))
# 	else:
# 		user_form = UserUpdateForm(instance=request.user)
# 		profile_form = ProfileUpdateForm(instance=request.user.profile)
		
# 		context = {
#         'user_form': user_form,
#         'profile_form': profile_form
#     }
# 	return render(request, 'account/profile.html', {
# 		 'user_form': user_form,
# 		 'profile_form': profile_form
#     })



