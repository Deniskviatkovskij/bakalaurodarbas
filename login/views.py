from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to a success page
            return redirect('dashboard')
        else:
            # return an error message
            messages.error(request, 'Invalid login credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


        