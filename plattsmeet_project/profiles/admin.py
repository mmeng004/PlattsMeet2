from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'major','pronouns','hobbies','bio','photo'] #display on the admin page
    list_filter = ('major','hobbies')
    search_fields = ('user', 'major','hobbies')
