from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'firstname','lastname','major','pronouns','year','hobbies','bio','photo'] #display on the admin page
    list_filter = ('firstname','lastname','major','hobbies')
    search_fields = ('user','firstname','lastname','major','hobbies')


