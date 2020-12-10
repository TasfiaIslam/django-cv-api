import requests
from django.shortcuts import render,  redirect
from .forms import UserDataForm
# Create your views here.


def home(request):
    # login_url = requests.get('https://recruitment.fisdev.com/api/login/')
    # test_url = requests.get(
    #     'https://recruitment.fisdev.com/api/v0/recruiting-entities/')
    # final_url = requests.get(
    #     'https://recruitment.fisdev.com/api/v1/recruiting-entities/')
    return render(request, 'cvapp/home.html')


def LoginView(request):
    # If token was already acquired, redirect to home page
    if request.session.get('api_token', False):
        return redirect('home')

    # Get username and password from posted data, authenticate and
    # if successful save api token to session
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        r = requests.post('https://recruitment.fisdev.com/api/login/',
                          data={'username': username, 'password': password})
        if r.status_code == 200:
            response = r.json()
            token = response['token']
            # Save token to session
            request.session['api_token'] = token
        else:
            messages.error(request, 'Authentication failed')
            return redirect('login')
    else:
        return render(request, 'cvapp/login.html', {})
