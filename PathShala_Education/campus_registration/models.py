# MARK: This represents the CampusStudent Model that get register for the Campus Student
# Access for @ Admin - Staff - Campus Coordinator
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
import datetime

from resources.hash_encrypt import encrypt_val, hash_code_generator
from resources.send_mail import send_mail_with_template

from campus_courses.models import CampusCourse
from campus.models import Coordinator, Campus

from resources.utility import EmailType as mail_type
# ----------------------------------------------
# MARK: Quick Fix: Move to the Utility func
# Multiple tuple for different coordinator name based on different locations
# tuple contains the coordinator id ->(Unique field to the campus DB) and it's corresponding name
from rest_framework.exceptions import ValidationError


def coordinator_name(campus_code):
    campus = Campus.objects.filter(campus_code=campus_code).first()
    print(campus.coordinators.all().first().name)
    return campus.coordinators.all().first().name


# MARK: This function fetch all the campus available and makes the tuple

def campus_course_list():
    codes = []
    names = []
    lists = CampusCourse.objects.all()
    for each_course in lists:
        codes.append(each_course.course_id)
        names.append(each_course.course_name)

    course_tuple = zip(codes, names)
    return course_tuple


# MARK: This function fetch all the campus available and makes the tuple

def campus_list():
    codes = []
    names = []
    lists = Campus.objects.all()
    for eachCampus in lists:
        print("Campus Code****", eachCampus.campus_code)
        print("Campus Name****", eachCampus.campus_name)
        codes.append(eachCampus.campus_code)
        names.append(eachCampus.campus_name)

    campus_tuple = zip(codes, names)
    return campus_tuple


# -------------------------------------------
# TODO: Generate batch id func

def batch_id_gen(batch):
    return batch + "30A"


# Campus Registration Models for Campus Students @ Admin Mode

class CampusRegistration(models.Model):
    mobile_no = models.CharField(primary_key=True, max_length=10)
    email_id = models.EmailField(max_length=32, blank=False)
    first_name = models.CharField(max_length=62, blank=False, default=None)
    last_name = models.CharField(max_length=62, blank=False, default=None)
    is_registered_app = models.BooleanField(_("App Downloaded"), default=False)
    registration_date = models.DateField(_("Today's Date"), default=datetime.date.today)
    username = models.CharField(_("Student Username"), max_length=32, blank=False, unique=True)
    campus_id = models.CharField(choices=campus_list(), blank=False, max_length=10, default=None)
    coordinator_name = models.CharField(blank=False, max_length=64, default="")

    def save(self, *args, **kwargs):
        self.coordinator_name = coordinator_name(self.campus_id)
        super(CampusRegistration, self).save(*args, **kwargs)

    # todo: Concatenate func for 2 strings.
    def __str__(self):
        return self.username


# MODEL: - Registered Course
'''
---------------------------------
Schema Description:
--------------------------------- 
    -
    -
    -
    -
---------------------------------  
'''


class RegisteredCourse(models.Model):
    student_id = models.ForeignKey(CampusRegistration, related_name="registered_course",
                                   verbose_name=_("Campus Student"), on_delete=models.CASCADE, default=None,
                                   db_column="student_id")
    registration_date = models.DateField(_("Registration Date"), default=datetime.date.today)
    course_id = models.CharField(choices=campus_course_list(), max_length=30)
    batch_id = models.CharField(max_length=32, default=None)
    course_activation_id = models.CharField(max_length=64, default=None)

    def save(self, *args, **kwargs):
        self.batch_id = batch_id_gen(self.course_id)
        self.course_activation_id = encrypt_val(hash_code_generator())
        self.send_mail_with_object_model()
        super(RegisteredCourse, self).save(*args, **kwargs)

    # TODO: Modify the Course name sent in the mail.
    def send_mail_with_object_model(self):
        course_name_dict = dict(campus_course_list())
        print("Campus Name", course_name_dict[self.course_id])
        course_detail = {'first_name': self.student_id.first_name, 'last_name': self.student_id.last_name,
                         'course_name': course_name_dict[self.course_id],
                         'course_activation_id': self.course_activation_id, 'batch_id': self.batch_id,
                         'username': self.student_id.username,
                         'email_id': self.student_id.email_id,
                         }
        send_mail_with_template(mail_type.REGISTRATION, course_detail)
