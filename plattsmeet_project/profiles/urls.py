from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'profile' 

urlpatterns = [
	path('viewprofile/', views.profile_view, name='viewprofile'),
	path('createprofile/', views.update_profile, name='createprofile'),
	path('searchbymajor/', views.search_bymajor, name='searchbymajor'),
	path('searchbyhobbies/',views.search_byhobbies, name='searchbyhobbies'),
]

