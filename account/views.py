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


def handle_redirect(view_type, user_type):
    if view_type != user_type:
        if user_type == "student":
            return 'student_home'
        elif user_type == "teacher":
            return 'teacher_home'


def student_register(request):
    template_name = 'account/auth/student_register.html'
    form1 = RegistrationFormUser()
    form2 = RegistrationFormStudent()

    if request.method == 'POST':
        form1 = RegistrationFormUser(request.POST)
        form2 = RegistrationFormStudent(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            userprofile = Userprofile(user=user, user_type='student', profile_picture=form2.cleaned_data['profile_picture'])
            userprofile.save()
            return redirect('account:welcome_page')
        else:
            return render(request, 'account/auth/student_register.html', {'form1': form1, 'form2': form2})

    return render(request, template_name, context={'form1': form1, 'form2': form2})


@login_required
def edit_student_profile(request):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
    template_name = 'account/auth/edit_student_profile.html'

    if request.method == 'POST':
        form1 = UserEditForm(request.POST, instance=request.user)
        form2 = RegistrationFormStudent(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            request.user.username = form1.cleaned_data['username']
            request.user.email = form1.cleaned_data['email']
            request.user.first_name = form1.cleaned_data['first_name']
            request.user.last_name = form1.cleaned_data['last_name']
            request.user.save()
            if form2.cleaned_data["profile_picture"]:
                request.user.userprofile.profile_picture = form2.cleaned_data['profile_picture']
                request.user.userprofile.save()

            return redirect('account:student_home')

        return render(request, template_name, {'form1': form1, 'form2': form2})

    form1 = UserEditForm(
        initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }
    )
    form2 = RegistrationFormStudent(initial={'profile_picture': request.user.userprofile.profile_picture})

    return render(request, template_name, {'form1': form1, 'form2': form2})


@login_required
def edit_teacher_profile(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
    template_name = 'account/auth/edit_student_profile.html'

    if request.method == 'POST':
        form1 = UserEditForm(request.POST, instance=request.user)
        form2 = RegistrationFormTeacher(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            request.user.username = form1.cleaned_data['username']
            request.user.email = form1.cleaned_data['email']
            request.user.first_name = form1.cleaned_data['first_name']
            request.user.last_name = form1.cleaned_data['last_name']
            request.user.save()
            if form2.cleaned_data["profile_picture"]:
                request.user.userprofile.profile_picture = form2.cleaned_data['profile_picture']
                request.user.userprofile.save()

            return redirect('account:student_home')

        return render(request, template_name, {'form1': form1, 'form2': form2})

    form1 = UserEditForm(
        initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }
    )
    form2 = RegistrationFormTeacher(initial={'profile_picture': request.user.userprofile.profile_picture})

    return render(request, template_name, {'form1': form1, 'form2': form2})


def teacher_register(request):
    template_name = 'account/auth/teacher_register.html'
    form1 = RegistrationFormUser()
    form2 = RegistrationFormTeacher()

    if request.method == 'POST':
        form1 = RegistrationFormUser(request.POST)
        form2 = RegistrationFormTeacher(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            userprofile = Userprofile(user=user, user_type='teacher', profile_picture=form2.cleaned_data['profile_picture'])
            userprofile.save()
            return redirect('account:welcome_page')
        else:
            return render(request, 'account/auth/teacher_register.html', {'form1': form1, 'form2': form2})

    return render(request, template_name, context={'form1': form1, 'form2': form2})


@login_required
def student_home(request):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = 'account/basic/student_home.html'

    return render(request, template_name, context={'user': request.user})


@login_required
def teacher_home(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = 'account/basic_teacher/teacher_home.html'
    
    return render(request, template_name, context={'user': request.user })


@login_required
def student_subclass_home(request, subclass_id):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = "account/basic/subclass_home.html"
    subclass = SubClass.objects.get(id=subclass_id)
    last_lessons = subclass.lesson_set.all().order_by("-date_added")[0:6]
    last_grades = request.user.userprofile.grade_set.filter(sub_class=subclass).order_by("-date_added")[0:6]
    return render(request, template_name, context={'last_lessons': last_lessons, "last_grades": last_grades, "sub_class": subclass})
    

@login_required
def student_lessons(request, subclass_id):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = "account/basic/student_lessons.html"
    search_input = request.GET.get('search')
    main_class = request.user.userprofile.main_class
    try:
        sub_class = SubClass.objects.get(id=subclass_id)
    except:
        sub_class = None

    if subclass_id == '0':
        lesson_list = Lesson.objects.filter(sub_class__main_class=main_class).order_by('-date_added')
    else:
        if SubClass.objects.filter(id=subclass_id):
            lesson_list = Lesson.objects.filter(sub_class=SubClass.objects.get(id=subclass_id), sub_class__main_class=main_class).order_by('-date_added')
        else:
            return redirect('account:student_home')
    if search_input:
        lesson_list = lesson_list.filter(Q(title__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__name__icontains=search_input))
        return render(request, template_name, context={'lessons': lesson_list, 'sub_class': sub_class})

    paginator = Paginator(lesson_list, 25)

    page = request.GET.get('page')
    lessons = paginator.get_page(page)

    return render(request, template_name, context={'lessons': lessons, 'sub_class': sub_class})


@login_required
def teacher_lessons(request, subclass_id):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    try:
        sub_class = SubClass.objects.get(id=subclass_id)
    except:
        sub_class = None

    template_name = "account/basic_teacher/teacher_lessons.html"
    search_input = request.GET.get('search')
    teacher = request.user.userprofile

    if subclass_id == '0':
        lesson_list = Lesson.objects.filter(sub_class__teacher=teacher).order_by('-date_added')
    else:
        if SubClass.objects.filter(id=subclass_id):
            lesson_list = Lesson.objects.filter(sub_class=SubClass.objects.get(id=subclass_id), sub_class__teacher=teacher).order_by('-date_added')
        else:
            return redirect('account:teacher_home')
    if search_input:
        lesson_list = lesson_list.filter(Q(title__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__main_class__name__icontains=search_input))
        return render(request, template_name, context={'lessons': lesson_list, 'subclass_id': subclass_id, 'sub_class': sub_class})

    paginator = Paginator(lesson_list, 25)

    page = request.GET.get('page')
    lessons = paginator.get_page(page)

    return render(request, template_name, context={'lessons': lessons, 'subclass_id': subclass_id, 'sub_class': sub_class})


@login_required
def add_lesson(request, subclass_id):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = 'account/basic_teacher/add_lesson.html'
    
    if not(SubClass.objects.filter(id=subclass_id, teacher=request.user.userprofile)) and subclass_id != '0':
        return redirect('account:teacher_lessons', '0')
    sub_classes = SubClass.objects.filter(teacher=request.user.userprofile)
    form = AddLessonForm(sub_classes=sub_classes)
    sub_class = 0

    if subclass_id != '0':
        sub_class = SubClass.objects.get(id=subclass_id)

    if request.method == 'POST':
        if subclass_id != '0':
            request.POST = request.POST.copy()
            request.POST['sub_class'] = str(sub_class.id)
        form = AddLessonForm(request.POST, request.FILES, sub_classes=sub_classes)
        if form.is_valid():
            lesson = Lesson(title=form.cleaned_data['title'], text=form.cleaned_data['text'], pdf=form.cleaned_data['pdf'], sub_class=form.cleaned_data['sub_class'])
            lesson.save()
            return redirect('account:teacher_lessons', subclass_id)
        else:
            return render(request, template_name, context={'form':form, 'sub_class': sub_class})
    
    return render(request, template_name, context={'form':form, 'sub_class': sub_class})


@login_required
def remove_confirm_lesson(request, subclass_id, lesson_id):
    template_name = 'account/basic_teacher/remove_confirm_lesson.html'
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except:
        return redirect('account:teacher_lessons', 0)
    
    return render(request, template_name, {'lesson': lesson})

@login_required
def remove_lesson(request, subclass_id, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except:
        return redirect('acccount:teacher_home')

    if lesson.sub_class.teacher == request.user.userprofile:
        lesson.delete()
    
    return redirect('account:teacher_lessons', 0)
    

@login_required
def student_lesson(request, subclass_id, lesson_id):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = "account/basic/student_lesson.html"

    if Lesson.objects.filter(id=lesson_id):
        if request.user.userprofile.main_class != Lesson.objects.get(id=lesson_id).sub_class.main_class:
            return redirect('account:student_lessons', "0")
    else:
        return redirect('account:student_lessons', "0")

    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, template_name, {'lesson': lesson})


@login_required
def teacher_lesson(request, subclass_id, lesson_id):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
    try:
        lesson = Lesson.objects.get(id=lesson_id, sub_class__teacher=request.user.userprofile)

    except:
        return redirect('account:teacher_lessons', "0")

    template_name = "account/basic_teacher/teacher_lesson.html"
    
    return render(request, template_name, {'lesson': lesson})


@login_required
def student_grades(request, subclass_id):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = "account/basic/student_grades.html"
    search_input = request.GET.get('search_grades')


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

    paginator = Paginator(grades_list, 48)

    page = request.GET.get('page')
    grades = paginator.get_page(page)

    return render(request, template_name, context={'grades': grades, 'subclass_id': subclass_id})


@login_required
def student_calendar(request, subclass_id, week):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
        
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
    

@login_required
def mainclass_home(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
    if not request.user.userprofile.main_class:
        return redirect('account:teacher_home')
    template_name = 'account/basic_teacher/mainclass_home.html'

    return render(request, template_name)


@login_required
def add_mainclass(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)
    if request.user.userprofile.main_class:
        return redirect('account:teacher_home')
    template_name = 'account/basic_teacher/add_mainclass.html'

    if request.method == 'POST':
        form = AddMainClassForm(request.POST)

        if form.is_valid():
            main_class = MainClass(name=form.cleaned_data['name'], semester=form.cleaned_data['semester'])
            main_class.save()
            request.user.userprofile.main_class = main_class
            request.user.userprofile.save()

            return redirect('account:mainclass_home')

    form = AddMainClassForm(initial={'semester': 1})
    return render(request, template_name, {'form': form})


@login_required
def edit_mainclass(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)

    template_name = 'account/basic_teacher/add_mainclass.html'

    if request.method == 'POST':
        form = AddMainClassForm(request.POST)

        if form.is_valid():
            main_class = request.user.userprofile.main_class
            main_class.name = form.cleaned_data['name']
            main_class.semester = form.cleaned_data['semester']
            main_class.save()

            return redirect('account:mainclass_home')

    form = AddMainClassForm(
            initial={
                'semester': request.user.userprofile.main_class.semester,
                'name': request.user.userprofile.main_class.name
            })

    return render(request, template_name, {'form': form})


@login_required
def add_subclass_request(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)   
    if not request.user.userprofile.main_class:
        return redirect('account:teacher_home')

    template_name = 'account/basic_teacher/add_subclass.html'
    
    if request.method == 'POST':
        form = AddSubClassForm(request.POST)
 
        if form.is_valid():
            try:
                Userprofile.objects.get(id=form.cleaned_data['teacher'], user_type='teacher')
            except:
                return render(request, template_name, {'form': AddSubClassForm(), 'invalid_id': True})
            request = Request(sent_by=request.user.userprofile, recieved_by=Userprofile.objects.get(id=form.cleaned_data['teacher']), subclass_name=form.cleaned_data['name'], subclass_color_code=form.cleaned_data['color_code'])
            request.save()
            return redirect('account:mainclass_home')
    
    return render(request, template_name, {'form': AddSubClassForm()})


@login_required
def edit_subclass(request, subclass_id):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)   
    if not request.user.userprofile.main_class.subclass_set.filter(id=subclass_id, main_class=request.user.userprofile.main_class):
        return redirect('account:teacher_home')

    template_name = 'account/basic_teacher/add_subclass.html'
    
    sub_class = SubClass.objects.get(id=subclass_id)

    if request.method == 'POST':
        form = AddSubClassForm(request.POST)
 
        if form.is_valid():
            try:
                teacher = Userprofile.objects.get(id=form.cleaned_data['teacher'], user_type='teacher')
            except:
                return render(request, template_name, {'form': AddSubClassForm( initial={'name': sub_class.name, 'color_code': sub_class.color_code }), 'invalid_id': True})

            if teacher != sub_class.teacher:
                try:
                    current_request = Request.objects.get(subclass=sub_class)
                    current_request.delete()
                except:
                    pass
                sub_class.teacher = None
                request = Request(sent_by=request.user.userprofile, recieved_by=teacher, subclass=sub_class)
                request.save()
            
            sub_class.name = form.cleaned_data['name']
            sub_class.color_code = form.cleaned_data['color_code']
            sub_class.save()

            return redirect('account:mainclass_home')

    if sub_class.teacher:
        return render(request, template_name, {'form': AddSubClassForm( initial={'name': sub_class.name, 'color_code': sub_class.color_code, 'teacher': sub_class.teacher.id })})
    try:
        teacher_id = Request.objects.get(subclass=sub_class).recieved_by.id
    except:
        teacher_id = None
    return render(request, template_name, {'form': AddSubClassForm( initial={'name': sub_class.name, 'color_code': sub_class.color_code, 'teacher': teacher_id })})


@login_required
def mainclass_students(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)   
    if not request.user.userprofile.main_class:
        return redirect('account:teacher_home')
    template_name = 'account/basic_teacher/mainclass_students.html'

    students = request.user.userprofile.main_class.userprofile_set.filter(user_type="student")

    return render(request, template_name, {'students': students})


@login_required
def kick_student(request, student_id):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)   
    if not request.user.userprofile.main_class:
        return redirect('account:teacher_home')
    
    try:
        student = Userprofile.objects.get(id=student_id)
        student.main_class = None
        student.save()
        return redirect('account:mainclass_students')

    except:
        return redirect('account:mainclass_students')


@login_required
def teacher_notifications(request):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)   
    template_name = 'account/basic_teacher/notifications.html'

    return render(request, template_name)


@login_required
def teacher_handle_request(request, request_id, handle):
    rd = handle_redirect('teacher', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd)  
    request_object = Request.objects.get(id=request_id)
    if request.user.userprofile == request_object.recieved_by and handle == '1':
        sub_class = SubClass(
            name=request_object.subclass_name,
            main_class=request_object.sent_by.main_class,
            color_code=request_object.subclass_color_code,
            teacher=request.user.userprofile,
        ) 
        sub_class.save()
        request_object.delete()
        return redirect('account:teacher_lessons', sub_class.id)
    elif request.user.userprofile == request_object.recieved_by and handle == '0':
        request_object.delete()
    
    elif request.user.userprofile == request_object.recieved_by and handle == '2':
        request_object.sent_by.main_class = request.user.userprofile.main_class
        request_object.sent_by.save()
        request_object.delete()
        return redirect('account:teacher_notifications')
    
    elif request.user.userprofile == request_object.recieved_by and handle == '3':
        request_object.subclass.teacher = request.user.userprofile
        request_object.subclass.save()
        request_object.delete()
        return redirect('account:teacher_notifications')

    return redirect('account:teacher_notifications')


@login_required
def student_join_request(request):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd) 
    if request.user.userprofile.main_class:
        return redirect('account:student_home')
    template_name = 'account/basic/join_class.html'

    if request.method == 'POST':
        try:
            main_class = MainClass.objects.get(id=request.POST['mainclass_id'])
        except:
            return render(request, template_name,{'id_valid': False})
        for past_request in Request.objects.filter(sent_by=request.user.userprofile):
            past_request.delete()
        request_object = Request(sent_by=request.user.userprofile, recieved_by=main_class.userprofile_set.get(user_type='teacher'))
        request_object.save()
        return redirect('account:student_home')
    
    return render(request, template_name,{'id_valid': True})


@login_required
def student_archives(request, subclass_id, my_filter):
    rd = handle_redirect('student', request.user.userprofile.user_type)
    if rd:
        return redirect('account:' + rd) 
    template_name = "account/basic/student_archives.html"
    search_input = request.GET.get('search')
    main_class = request.user.userprofile.main_class
    try:
        sub_class = SubClass.objects.get(id=subclass_id)
        if request.user.userprofile.main_class != sub_class.main_class:
            return redirect('account:student_home')
    except:
        sub_class = None
        if subclass_id != '0':
            return redirect('account:student_home')

    if my_filter == '0':
        if subclass_id == '0':
            archive_list = Archive.objects.filter(author=request.user.userprofile, archive_type='submission').order_by('-date_added')
        else:
            archive_list = Archive.objects.filter(sub_class=sub_class, author=request.user.userprofile, sub_class__main_class=main_class, archive_type='submission').order_by('-date_added')
    
        if search_input:
            archive_list = archive_list.filter(Q(title__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__name__icontains=search_input))
            return render(request, template_name, context={'archives': archive_list, 'sub_class': sub_class, 'my_filter': my_filter})
    else:
        if subclass_id == '0':
            archive_list = Archive.objects.filter(sub_class__main_class=main_class, author=request.user.userprofile, archive_type='private').order_by('-date_added')
        else:
            archive_list = Archive.objects.filter(sub_class=sub_class, author=request.user.userprofile, sub_class__main_class=main_class, archive_type='private').order_by('-date_added')
    
        if search_input:
            archive_list = archive_list.filter(Q(title__icontains=search_input) | Q(date_added__icontains=search_input) | Q(sub_class__name__icontains=search_input))
            return render(request, template_name, context={'archives': archive_list, 'sub_class': sub_class, 'my_filter': 1})

    paginator = Paginator(archive_list, 25)

    page = request.GET.get('page')
    archives = paginator.get_page(page)

    return render(request, template_name, context={'archives': archives, 'sub_class': sub_class, 'my_filter': my_filter})


