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
from accounts.models import Account


#delete account view
def delete_account(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("User does not exist .")
	if account:
		account.delete()
		messages.success(request, 'Your account was successfully deleted!')
	return redirect('home')

#Based on the tutorial from #https://codingwithmitch.com/courses/real-time-chat-messenger/
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


#Based on the tutorial from #https://codingwithmitch.com/courses/real-time-chat-messenger/
#view account view
def account_view(request, *args, **kwargs):
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
		context['hometown'] = profile.hometown
		

		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends

		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value 
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
			
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id

				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
			
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html",context)




#works search accounts
@login_required
def account_search(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(username__icontains=search_query).distinct() 
			user = request.user
			accounts = [] 
			for account in search_results:
				accounts.append((account, False)) 
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





