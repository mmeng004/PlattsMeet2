from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'profile' 

#urlpatterns = [
 # post views
 #path('login/', views.user_login, name='login'),
 #path('login/', views.userlogin, name='login'),
# path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 #path('register/', views.register, name='register'),
 #path('edit/', views.edit, name='edit'),

 #path('<user_id>/',views.account_view, name = 'accountviews'),}

urlpatterns = [
	#path('<user_id>/', views.view_profile, name='view'),
	path('createprofile/', views.update_profile, name='createprofile'),
	#path('<user_id>/viewprofile/', views.view_profile, name='viewprofile'),
	
]

