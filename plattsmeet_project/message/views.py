#Adapted from on the tutorial from https://www.youtube.com/watch?v=oxrQdZ5KqW0  
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View
from .models import Message, MessageThread
from .forms import ThreadForm, MessageForm
from django.utils import timezone
from accounts.models import Account

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = Message.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'message/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'message/create_message.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = Account.objects.get(username=username)
            if Message.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Message.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('message:thread', pk=thread.pk)
            elif Message.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Message.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('message:thread', pk=thread.pk)

            if form.is_valid():
                thread = Message(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('message:thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('message:create-thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = Message.objects.get(pk=pk)
        message_list = MessageThread.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'message/messages.html', context)

class CreateMessage(View):
        def post(self, request, pk, *args, **kwargs):
            thread = Message.objects.get(pk=pk)
            if thread.receiver == request.user:
                receiver = thread.user
            else:
                receiver = thread.receiver

            message = MessageThread(
                thread=thread,
                sender_user=request.user,
                receiver_user=receiver,
                body=request.POST.get('message')
            )

            message.save()
            return redirect('message:thread', pk=pk)




