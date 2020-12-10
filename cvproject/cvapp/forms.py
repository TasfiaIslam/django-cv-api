from django import forms


class UserDataForm(forms.Form):
    name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(max_length=14, required=True)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=256, required=True)
    graduation_year = forms.IntegerField(required=True)
    cgpa = forms.FloatField()
    experience_in_months = forms.IntegerField()
    current_work_place_name = forms.CharField()
    applying_in = forms.CharField()
    expected_salary = forms.IntegerField()
    field_buzz_reference = forms.CharField()
    github_project_url = forms.CharField()
    cv_file = forms.FileField()
