# MARK: This represents the CampusStudent Model that get register for the Campus Student
# Access for @ Admin - Staff - Campus Coordinator
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
import datetime
from campus.models import Coordinator, Campus
from resources.views import send_mail_func
from resources.views import decrypt_val, encrypt_val
from resources.views import hash_code_generator

# ----------------------------------------------
# MARK: Quick Fix: Move to the Utility func
# Multiple tuple for different coordinator name based on different locations
# tuple contains the coordinator id ->(Unique field to the campus DB) and it's corresponding name
from rest_framework.exceptions import ValidationError


def coordinator_name(campus_code):
    campus = Campus.objects.filter(campus_code=campus_code).first()
    print(campus.coordinators.all().first().name)
    return campus.coordinators.all().first().name

COURSE_ID = [
    ("ID-1", "Course 1"),
    ("ID-2", "Course 2"),
    ("ID-3", "Course 3"),
    ("ID-4", "Course 4"),
]


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
# TODO: add "campus" field that will the be the pk of Campus DB schema.
# TODO: Automated Field: modify the "coordinator" field to the automated field. fetch the current coordinator name from the cmapus_db pk

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
    course_id = models.CharField(choices=COURSE_ID, max_length=30)
    batch_id = models.CharField(max_length=32, default=None)
    course_activation_id = models.CharField(max_length=64, default=None)

    def save(self, *args, **kwargs):
        self.batch_id = batch_id_gen(self.course_id)
        self.course_activation_id = encrypt_val(hash_code_generator())
        self.send_mail_with_object_model()
        super(RegisteredCourse, self).save(*args, **kwargs)

    # TODO: MARK: Send Mail for this current object created
    # todo: Modify the Course name sent in the mail.
    def send_mail_with_object_model(self):
        mail_to_address = self.student_id.email_id
        subject_string = "Course Activation Message"
        message_body = "Hi {}, \nThank you for registering with the {} course.\nHappy Learning! Please find the " \
                       "secret activation code below for app registration. \n*Please Keep the code secret. \nCourse " \
                       "Activation ID: {}".format(
            self.student_id.first_name + " " + self.student_id.last_name, self.course_id,
            decrypt_val(self.course_activation_id))
        print("to", mail_to_address, "body:  ", message_body)
        print(send_mail_func(to=mail_to_address, message=message_body, subject=subject_string))
