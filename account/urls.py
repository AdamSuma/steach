from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = 'account'

urlpatterns = [
    url(r'^$', LoginView.as_view(template_name='account/welcome.html'), name='welcome_page'),
    url(r'^student/$', views.student_home, name='student_home'),
    url(r'^student/(?P<subclass_id>[0-9]+)/$', views.student_subclass_home, name='student_subclass_home'),
    url(r'^student/lessons/(?P<subclass_id>[0-9]+)/$', views.student_lessons, name='student_lessons'),    
    url(r'^student/grades/(?P<subclass_id>[0-9]+)/$', views.student_grades, name='student_grades'),
    url(r'^student/calendar/(?P<subclass_id>[0-9]+)/(?P<week>[0-9]+)/$', views.student_calendar, name='student_calendar'),    
    url(r'^student/lessons/(?P<subclass_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.student_lesson, name='student_lesson'),
    url(r'^student_register/$', views.student_register, name='student_register'),
    url(r'^teacher_register/$', views.teacher_register, name='teacher_register'),
]