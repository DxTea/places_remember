from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('places:places')
    return render(request, 'welcome_page.html')
