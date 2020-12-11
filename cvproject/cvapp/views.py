import requests
import uuid
import time
import json
from django.shortcuts import render,  redirect
from django.contrib import messages
from .forms import UserDataForm
# Create your views here.

# login_url = requests.get('https://recruitment.fisdev.com/api/login/')
# test_url = requests.get(
#     'https://recruitment.fisdev.com/api/v0/recruiting-entities/')
# final_url = requests.get(
#     'https://recruitment.fisdev.com/api/v1/recruiting-entities/')


def home(request):
    return render(request, 'cvapp/home.html')


def LoginView(request):
    # If token was already acquired, redirect to home page
    # if request.session.get('api_token', False):
    #     del request.session['api_token']
    #     return redirect('home')

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
            return render(request, 'cvapp/user_form.html')
        else:
            messages.error(request, 'Authentication failed')
            return redirect('login')

    else:
        return render(request, 'cvapp/login.html', {})


def UserDataView(request):
    form = UserDataForm()

    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():

            token = request.session['api_token']

            on_spot_created_time = int(round(time.time() * 1000))
            on_spot_updated_time = int(round(time.time() * 1000))
            tsync_id = str(uuid.uuid4())
            cv_tsync_id = str(uuid.uuid4())

            file = request.FILES['cv_file']
            files = {'file': file.read()}

            # json_data = json.loads(request.body)
            headers = {'content-type': 'application/json',
                       'Authorization': f'Token {token}'}

            userData = {"tsync_id": tsync_id,
                        "name": form.data['name'],
                        "email": form.data['email'],
                        "phone": form.data['phone'],
                        "full_address": form.data['full_address'],
                        "name_of_university": form.data['name_of_university'],
                        "graduation_year": form.data['graduation_year'],
                        "cgpa": form.data['cgpa'],
                        "experience_in_months": form.data['experience_in_months'],
                        "current_work_place_name": form.data['current_work_place_name'],
                        "applying_in": form.data['applying_in'],
                        "expected_salary": form.data['expected_salary'],
                        "field_buzz_reference": form.data['field_buzz_reference'],
                        "github_project_url": form.data['github_project_url'],
                        "cv_file": {
                            "tsync_Id": cv_tsync_id},
                        "on_spot_created_time": on_spot_created_time,
                        "on_spot_updated_time": on_spot_updated_time,
                        }

            r = requests.post(
                "https://recruitment.fisdev.com/api/v1/recruiting-entities/", data=userData, headers=headers)

            if r.status_code == 200:
                response = r.json()

                FILE_TOKEN_ID = response['cv_file']['id']
                headers = {'content-type': 'application/pdf',
                           'Authorization': f'Token {token}'}
                file_url = "https://recruitment.fisdev.com/api/file-object/{FILE_TOKEN_ID}/"

                file = request.FILES['cv_file']
                files = {'file': file.read()}

                r = requests.post(
                    file_url, files=files, headers=headers)

                if r.status_code == 200:
                    messages.success(request, 'Form submission successful')
                    return redirect('home')

    context = {'form': form}
    return render(request, 'cvapp/user_form.html', context)
