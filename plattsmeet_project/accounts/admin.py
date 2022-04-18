from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account ,Profile

admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'major','pronouns','hobbies','bio','photo']
    search_fields = ('email','username',)

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)

