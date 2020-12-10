from django import forms
from django.core.exceptions import ValidationError


class UserDataForm(forms.Form):

    CHOICES = (
        ('mobile', 'mobile'),
        ('backend', 'backend'),
    )

    tsync_id = forms.UUIDField(max_length=55, required=True)

    name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(max_length=14, required=True)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=256, required=True)
    graduation_year = forms.IntegerField(required=True)
    cgpa = forms.FloatField(min_value=2.0, max_value=4.0, required=False)

    experience_in_months = forms.IntegerField(
        min_value=0, max_value=100, required=False)
    current_work_place_name = forms.CharField(max_length=256, required=False)
    applying_in = forms.Select(choices=CHOICES)

    expected_salary = forms.IntegerField(
        min_value=15000, max_value=60000, required=True)
    field_buzz_reference = forms.CharField(max_length=256, required=False)
    github_project_url = forms.CharField(max_length=512, required=True)

    # cv_file = forms.FileField()
    # cv_file.tsync_id = forms.CharField()

    on_spot_update_time = forms.DateTimeField()
    on_spot_creation_time = forms.DateTimeField()
