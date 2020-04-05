from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator
from datetime import date

def profile_image_path(instance, filename):
    return 'user_profiles/{}'.format(filename)

def certificate_file_path(instance, filename):
    return 'teacher_certificates/{}_{}'.format(instance, date.today())


class MainClass(models.Model):
    name = models.CharField(max_length=8)
    semester = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name
    

class Userprofile(models.Model):
    TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    #__________ MAIN ATTRIBUTES ____________
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to=profile_image_path, blank=True, null=True)
    main_class = models.ForeignKey(MainClass, on_delete=models.SET_NULL, null=True, blank=True)   

    #___________ STUDENT ___________________
    
    id_number = models.IntegerField(blank=True, null=True) 
    
    #___________ TEACHER ___________________
    
    teaching_subject = models.CharField(max_length=100, blank=False, null=True)
    teaching_certificate = models.FileField(upload_to=certificate_file_path, blank=True, null=True)
    


    def __str__(self):
        return self.user.username + " " + "Profile"


class SubClass(models.Model):
    name = models.CharField(max_length=20,blank=False,  null=False)
    subject = models.CharField(max_length=40, blank=True, null=True)
    teacher = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True)
    main_class = models.ForeignKey(MainClass, on_delete=models.CASCADE, null=False)
    color_code = models.CharField(max_length=6, default="C70000")

    def __str__(self):
        return self.main_class.name + " " + self.name
    


class Lesson(models.Model):
    title = models.TextField(max_length=100)
    sub_class = models.ForeignKey(SubClass, on_delete=models.CASCADE, null=False)
    text = models.TextField(max_length=1000)
    date_added = models.DateField(auto_now_add=True)

    def pdf_upload_path(self, filename):
        return "lessons/" + self.sub_class.main_class.name + "/" + self.sub_class.name + "/" + filename

    pdf = models.FileField(upload_to=pdf_upload_path, null=True, blank=True)

    def __str__(self):
        return self.title



class Grade(models.Model):
    actual_value = models.FloatField(validators=[MaxValueValidator(10)], null=True, blank=True)
    value = models.IntegerField(validators=[MaxValueValidator(10)])
    is_term_paper = models.BooleanField(default=False)
    student = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=False)
    sub_class = models.ForeignKey(SubClass, on_delete=models.CASCADE, null=False)
    date_added = models.DateField(default=date.today)



class Event(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    sub_class = models.ForeignKey(SubClass, on_delete=models.CASCADE, null=False)
    description = models.TextField(max_length=250, null=True, blank=True)
    
    TYPE_CHOICES = (
        ('test', 'Test'),
        ('project', 'Project'),
        ('homework', 'Homework')
    )

    event_type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True)

    def test_pdf_upload_path(self, filename):
        return "events/" + self.sub_class.main_class.name + "/" + self.sub_class.name + "/" + filename

    topics = models.FileField(upload_to=test_pdf_upload_path, null=True, blank=True)


class Request(models.Model):
    sent_by = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=False, related_name='sent')
    recieved_by = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=False, related_name='recieved')
    subclass_name = models.CharField(max_length=20,blank=False,  null=False)
    subclass_color_code = models.CharField(max_length=6, default="C70000")
    subclass = models.OneToOneField(SubClass, on_delete=models.CASCADE, null=True, default=None)


class Archive(models.Model):
    TYPE_CHOICES = (
        ('submission', 'Submission'),
        ('private', 'Private')
    )

    title = models.TextField(max_length=100)
    author = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=False)
    sub_class = models.ForeignKey(SubClass, on_delete=models.CASCADE, null=False)
    text = models.TextField(max_length=1000)
    date_added = models.DateField(auto_now_add=True)
    archive_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='private')

    def pdf_upload_archive_path(self, filename):
        return "archives/" + filename

    pdf = models.FileField(upload_to=pdf_upload_archive_path, null=True, blank=True)

    def __str__(self):
        return self.title











