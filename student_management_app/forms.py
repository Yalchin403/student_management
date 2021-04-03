from django import forms 
from django.forms import Form
from student_management_app.models import Group, SessionYearModel, Subjects


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['subject_id'] = forms.ModelMultipleChoiceField(label="Subjects", queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple)
        self.fields['group_id'] = forms.ModelMultipleChoiceField(label="Group", queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
        self.fields['session_year_id'] = forms.ChoiceField(label="Session Year", choices=[(session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year)) for session_year in SessionYearModel.objects.all()], widget=forms.Select(attrs={"class":"form-control"}))

class AddStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)
        self.fields['group_id'] = forms.ModelMultipleChoiceField(label="Groups", queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
        

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        self.fields['subject_id'] = forms.ModelMultipleChoiceField(label="Subjects", queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple)
        self.fields['group_id'] = forms.ModelMultipleChoiceField(label="Group", queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
        self.fields['session_year_id'] = forms.ChoiceField(label="Session Year", choices=[(session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year)) for session_year in SessionYearModel.objects.all()], widget=forms.Select(attrs={"class":"form-control"}))