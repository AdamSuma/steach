from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class RegistrationFormUser(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
        widgets = {
			'username': forms.TextInput(attrs={'style':'color:black;'}),
            'email': forms.TextInput(attrs={'style':'color:black;'}),
            'first_name': forms.TextInput(attrs={'style':'color:black;'}),
            'last_name': forms.TextInput(attrs={'style':'color:black;'}),
            'password1': forms.PasswordInput(attrs={'style':'color:black;'}),
            'password2': forms.PasswordInput(attrs={'style':'color:black;'}),
		}

    def save(self, commit=True):
        user = super(RegistrationFormUser, self).save(commit=False)

        if commit:
            user.save()

        return user


class RegistrationFormStudent(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = (
            'id_number',
            'profile_picture',
        )
        widgets = {
            'id_number': forms.TextInput(attrs={'style':'color:black;'}),
        }


class RegistrationFormTeacher(forms.ModelForm):
        
    class Meta:
        model = Userprofile
        fields = (
            'teaching_subject',
            'teaching_certificate',
            'profile_picture',
        )
        widgets = {
            'teacher_subject': forms.TextInput(attrs={'style':'color:black;'}),
        }

class AddLessonForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        self.sub_classes = kwargs.pop('sub_classes')
        super(AddLessonForm, self).__init__(*args, **kwargs)
        self.fields['sub_class'] = forms.ModelChoiceField(queryset=self.sub_classes, empty_label="Choose Class")
            

    class Meta:
        model = Lesson
        fields = (
            'title',
            'text',
            'pdf',
            'sub_class',
        )