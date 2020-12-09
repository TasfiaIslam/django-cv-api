from django import forms


class UserDataForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    full_address = forms.CharField()
    name_of_university = forms.CharField()
    graduation_year = forms.IntegerField()
    cgpa = forms.FloatField()
    experience_in_months = forms.IntegerField()
    current_work_place_name = forms.CharField()
    applying_in = forms.CharField()
    expected_salary = forms.IntegerField()
    field_buzz_reference = forms.CharField()
    github_project_url = forms.CharField()


class CvFileForm(forms.Form):
    cv_file = forms.FileField()
