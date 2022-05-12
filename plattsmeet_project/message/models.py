#Based on the tutorial from https://www.youtube.com/watch?v=oxrQdZ5KqW0 
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

	
class Message(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')

class MessageThread(models.Model):
	thread = models.ForeignKey('Message', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)

