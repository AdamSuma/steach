from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = 'account'

urlpatterns = [
    url(r'^$', LoginView.as_view(template_name='account/welcome.html'), name='welcome_page'),
    url(r'^logout/$', LogoutView.as_view(template_name='account/auth/logout.html'), name='logout'),
    url(r'^student/$', views.student_home, name='student_home'),
    url(r'^teacher/$', views.teacher_home, name='teacher_home'),
    url(r'^student/join_class/$', views.student_join_request, name='student_join_request'),
    url(r'^teacher/notifications/$', views.teacher_notifications, name='teacher_notifications'),
    url(r'^teacher/notifications/(?P<request_id>[0-9]+)/(?P<handle>[0-9]+)/$', views.teacher_handle_request, name='teacher_handle_request'),
    url(r'^teacher/add_mainclass/$', views.add_mainclass, name='add_mainclass'),
    url(r'^teacher/edit_mainclass/$', views.edit_mainclass, name='edit_mainclass'),
    url(r'^teacher/main_class/$', views.mainclass_home, name='mainclass_home'),
    url(r'^teacher/main_class/students/$', views.mainclass_students, name='mainclass_students'),
    url(r'^teacher/main_class/kick/(?P<student_id>[0-9]+)/$', views.kick_student, name='kick_student'),
    url(r'^teacher/main_class/add_subclass/$', views.add_subclass_request, name='add_subclass_request'),
    url(r'^teacher/main_class/(?P<subclass_id>[0-9]+)/edit/$', views.edit_subclass, name='edit_subclass'),
    url(r'^student/(?P<subclass_id>[0-9]+)/$', views.student_subclass_home, name='student_subclass_home'),
    url(r'^student/lessons/(?P<subclass_id>[0-9]+)/$', views.student_lessons, name='student_lessons'),
    url(r'^teacher/lessons/(?P<subclass_id>[0-9]+)/$', views.teacher_lessons, name='teacher_lessons'),
    url(r'^teacher/lessons/(?P<subclass_id>[0-9]+)/add_lesson/$', views.add_lesson, name='add_lesson'),
    url(r'^teacher/lessons/(?P<subclass_id>[0-9]+)/(?P<lesson_id>[0-9]+)/confirm_delete/$', views.remove_confirm_lesson, name='remove_confirm_lesson'),        
    url(r'^teacher/lessons/(?P<subclass_id>[0-9]+)/(?P<lesson_id>[0-9]+)/delete/$', views.remove_lesson, name='remove_lesson'),
    url(r'^student/grades/(?P<subclass_id>[0-9]+)/$', views.student_grades, name='student_grades'),
    url(r'^student/calendar/(?P<subclass_id>[0-9]+)/(?P<week>[0-9]+)/$', views.student_calendar, name='student_calendar'),    
    url(r'^student/lessons/(?P<subclass_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.student_lesson, name='student_lesson'),
    url(r'^teacher/lessons/(?P<subclass_id>[0-9]+)/(?P<lesson_id>[0-9]+)/$', views.teacher_lesson, name='teacher_lesson'),
    url(r'^student_register/$', views.student_register, name='student_register'),
    url(r'^student/edit/$', views.edit_student_profile, name='edit_student_profile'),
    url(r'^teacher_register/$', views.teacher_register, name='teacher_register'),
    url(r'^teacher/edit/$', views.edit_teacher_profile, name='edit_teacher_profile'),
    url(r'^student/archives/(?P<subclass_id>[0-9]+)/(?P<my_filter>[0-9]+)/$', views.student_archives, name='student_archives'),    
]