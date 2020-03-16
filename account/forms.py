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


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        widgets = {
			'username': forms.TextInput(attrs={'style':'color:black;'}),
            'email': forms.TextInput(attrs={'style':'color:black;'}),
            'first_name': forms.TextInput(attrs={'style':'color:black;'}),
            'last_name': forms.TextInput(attrs={'style':'color:black;'}),
		}


    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class RegistrationFormStudent(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = (
            'profile_picture',
        )


class RegistrationFormTeacher(forms.ModelForm):
        
    class Meta:
        model = Userprofile
        fields = (
            'profile_picture',
        )

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

class AddMainClassForm(forms.ModelForm):
    class Meta:
        model = MainClass
        fields = (
            'name',
            'semester',
        )

class AddSubClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSubClassForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.IntegerField()

    class Meta:
        model = SubClass
        fields = (
            'name',
            'color_code'
        )