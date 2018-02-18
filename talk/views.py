from django.shortcuts import render


def user_list(request):
    return render(request, 'talk/user_list.html')
