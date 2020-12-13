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

    token = request.session['api_token']
    # on_spot_created_time = int(round(time.time() * 1000))
    # on_spot_updated_time = int(round(time.time() * 1000))
    # tsync_id = str(uuid.uuid4())
    # cv_tsync_id = str(uuid.uuid4())
    form = UserDataForm()

    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():

            cv_get_file = request.FILES['cv_file']
            files = {'file': cv_get_file.read()}

            # json_data = json.loads(request.body)
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'Token {token}'}

            userData = {'tsync_id': tsync_id,
                        'name': request.POST.get('name'),
                        'email': request.POST.get('email'),
                        'phone': request.POST.get('phone'),
                        'full_address': request.POST.get('full_address'),
                        'name_of_university': request.POST.get('name_of_university'),
                        'graduation_year': request.POST.get('graduation_year'),
                        'cgpa': request.POST.get('cgpa'),
                        'experience_in_months': request.POST.get('experience_in_months'),
                        'current_work_place_name': request.POST.get('current_work_place_name'),
                        'applying_in': request.POST.get('applying_in'),
                        'expected_salary': request.POST.get('expected_salary'),
                        'field_buzz_reference': request.POST.get('field_buzz_reference'),
                        'github_project_url': request.POST.get('github_project_url'),
                        'cv_file': {
                            'tsync_Id': cv_tsync_id},
                        'on_spot_created_time': on_spot_created_time,
                        'on_spot_updated_time': on_spot_updated_time,
                        }

            cv_response = requests.post(
                'https://recruitment.fisdev.com/api/v0/recruiting-entities/', data=userData, headers=headers)

            data_response = cv_response.json()

            if cv_response.status_code == 200:
                messages.success(request, 'Form submission successful')
                response = r.json()

                FILE_TOKEN_ID = data_response['cv_file']['id']

                headers = {
                    'Authorization': f'Token {token}'}

                file_url = "https://recruitment.fisdev.com/api/file-object/{FILE_TOKEN_ID}/"

                get_file = request.FILES['cv_file']
                files = {'file': get_file.read()}

                file_request = request.put(
                    file_url, files=files, headers=headers)

                if file_request.status_code == 200:
                    messages.success(request, 'File submission successful')
                    return redirect('home')

    context = {'form': form}
    return render(request, 'cvapp/user_form.html', context)
