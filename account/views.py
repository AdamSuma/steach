from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import *
from django.core.paginator import Paginator
import datetime
from datetime import timedelta



def student_register(request):
    template_name = 'account/auth/student_register.html'
    form1 = RegistrationFormUser()
    form2 = RegistrationFormStudent()

    if request.method == 'POST':
        form1 = RegistrationFormUser(request.POST)
        form2 = RegistrationFormStudent(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            userprofile = Userprofile(user=user, user_type='student', id_number=form2.cleaned_data['id_number'], profile_picture=form2.cleaned_data['profile_picture'])
            userprofile.save()
            return redirect('account:welcome_page')
        else:
            return render(request, 'account/auth/student_register.html', {'form1': form1, 'form2': form2})

    return render(request, template_name, context={'form1': form1, 'form2': form2})


def teacher_register(request):
    template_name = 'account/auth/teacher_register.html'
    form1 = RegistrationFormUser()
    form2 = RegistrationFormTeacher()

    if request.method == 'POST':
        form1 = RegistrationFormUser(request.POST)
        form2 = RegistrationFormTeacher(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            userprofile = Userprofile(user=user, user_type='teacher', teaching_certificate=form2.cleaned_data['teaching_certificate'], teaching_subject=form2.cleaned_data['teaching_subject'], profile_picture=form2.cleaned_data['profile_picture'])
            userprofile.save()
            return redirect('account:welcome_page')
        else:
            return render(request, 'account/auth/teacher_register.html', {'form1': form1, 'form2': form2})

    return render(request, template_name, context={'form1': form1, 'form2': form2})


@login_required
def student_home(request):
    template_name = 'account/basic/student_home.html'
    if request.user.userprofile.user_type == 'teacher':
        return redirect('account:teacher_register')
    return render(request, template_name, context={'user': request.user})


@login_required
def student_subclass_home(request, subclass_id):
    if request.user.userprofile.user_type == 'teacher':
        return redirect('account:teacher_register')
    template_name = "account/basic/subclass_home.html"
    subclass = SubClass.objects.get(id=subclass_id)
    last_lessons = subclass.lesson_set.all().order_by("-date_added")[0:6]
    last_grades = request.user.userprofile.grade_set.filter(sub_class=subclass).order_by("-date_added")[0:6]
    return render(request, template_name, context={'last_lessons': last_lessons, "last_grades": last_grades, "sub_class": subclass})
    

@login_required
def student_lessons(request, subclass_id):
    template_name = "account/basic/student_lessons.html"
    search_input = request.GET.get('search')
    if request.user.userprofile.user_type == 'teacher':
        return redirect('account:teacher_register')
    main_class = request.user.userprofile.main_class

    if subclass_id == '0':
        lesson_list = Lesson.objects.filter(sub_class__main_class=main_class).order_by('-date_added')
    else:
        if SubClass.objects.filter(id=subclass_id):
            lesson_list = Lesson.objects.filter(sub_class=SubClass.objects.get(id=subclass_id), sub_class__main_class=main_class).order_by('-date_added')
        else:
            return redirect('account:student_home')
    if search_input:
        lesson_list = lesson_list.filter(Q(title__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__name__icontains=search_input))
        return render(request, template_name, context={'lessons': lesson_list, 'subclass_id': subclass_id})

    paginator = Paginator(lesson_list, 25)

    page = request.GET.get('page')
    lessons = paginator.get_page(page)

    return render(request, template_name, context={'lessons': lessons, 'subclass_id': subclass_id})


@login_required
def student_lesson(request, subclass_id, lesson_id):
    template_name = "account/basic/student_lesson.html"

    if Lesson.objects.filter(id=lesson_id):
        if request.user.userprofile.main_class != Lesson.objects.get(id=lesson_id).sub_class.main_class:
            return redirect('account:student_lessons', "0")
    else:
        return redirect('account:student_lessons', "0")

    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, template_name, {'lesson': lesson})


@login_required
def student_grades(request, subclass_id):
    template_name = "account/basic/student_grades.html"
    search_input = request.GET.get('search_grades')

    if request.user.userprofile.user_type == 'teacher':
        return redirect('account:teacher_register')
    main_class = request.user.userprofile.main_class

    if subclass_id == '0':
        grades_list = Grade.objects.filter(sub_class__main_class=main_class, student=request.user.userprofile).order_by('-date_added')
    else:
        if SubClass.objects.filter(id=subclass_id):
            grades_list = Grade.objects.filter(sub_class=SubClass.objects.get(id=subclass_id), student=request.user.userprofile).order_by('-date_added')
        else:
            return redirect('account:student_home')
    if search_input:
        grades_list = grades_list.filter(Q(value__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__name__icontains=search_input))
        return render(request, template_name, context={'grades': grades_list, 'subclass_id': subclass_id})
        print(grades_list)

    paginator = Paginator(grades_list, 25)

    page = request.GET.get('page')
    grades = paginator.get_page(page)

    return render(request, template_name, context={'grades': grades, 'subclass_id': subclass_id})


@login_required
def student_calendar(request, subclass_id, week):
    week = int(week)
    template_name = "account/basic/student_calendar.html"
    today = datetime.date.today()
    main_class = request.user.userprofile.main_class
    sub_class = SubClass.objects.filter(id=subclass_id)

    if week and (today.weekday() in [5,6]):
        delta = timedelta(days=7-today.weekday() + 7*(week))
        date_start = today + delta
    elif week:
        delta = timedelta(days=7-today.weekday() + 7*(week-1))
        date_start = today + delta
    elif today.weekday() >= 5:
        date_start = today + timedelta(7-today.weekday())
    else:
        date_start = today
    
    dates = {}
    dates2 = []
    if sub_class:
        for i in range(date_start.weekday(), 5):
            date = date_start + timedelta(days=(i-today.weekday()))
            events = Event.objects.filter(date=date, sub_class=sub_class[0])

            dates.update({ date:events })

        return render(request, template_name, context={'dates': dates, 'sub_class': sub_class[0]})
    
    else:
        for i in range(date_start.weekday(), 5):
            date = date_start + timedelta(days=(i-date_start.weekday()))
            events = Event.objects.filter(date=date, sub_class__main_class=main_class)

            dates.update({ date:events })

        return render(request, template_name, context={'dates': dates, 'dates2': dates2})
    
