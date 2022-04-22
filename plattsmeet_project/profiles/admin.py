from django.contrib import admin

from .models import Profile

admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'major','pronouns','hobbies','bio','photo']
    search_fields = ('email','username',)

# Register your models here.
