from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect


def user_list(request):
    return render(request, 'talk/user_list.html')

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('user_list'))
        else:
            print(form.errors)
    return render(request, 'talk/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('log_in'))