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
from django.contrib.auth.decorators import login_required



#works register
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

#works logout
def logoutview(request):
	logout(request)
	return redirect("home")
#works login
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


#view account
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
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		is_self = True
		is_friend = False

		user = request.user

		if user.is_authenticated and user != account:
			is_self = False
		elif not user.is_authenticated:
			is_self = False

		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html", context)


@login_required
def update_account(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		if user_form.is_valid():
			user_form.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('portalpage')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		user_form = UserUpdateForm(request.POST, instance=request.user)
		context = {
        'user_form': user_form,
    }
	return render(request, 'accounts/edit.html', {
		  'user_form': user_form,
    })



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



