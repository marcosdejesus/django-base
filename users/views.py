from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import SignUpForm

# Create your views here.
def signup(request, redirect_url):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(redirect_url)
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html',{'form':form})
