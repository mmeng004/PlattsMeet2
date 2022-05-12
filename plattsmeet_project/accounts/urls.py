from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account' 

urlpatterns = [
	path('<user_id>/', views.account_view, name="view"),
	path('<user_id>/delete/', views.delete_account, name='delete'),
	path('<user_id>/edit/', views.edit_account, name='edit'),

]

