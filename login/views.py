from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # perkelti i perziuros puslapi
            return redirect('dashboard')
        else:
            # atvaizduoti klaida
            messages.error(request, 'Invalid login credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


        