# MARK: This represents the CampusStudent Model that get register for the Campus Student
# Access for @ Admin - Staff - Campus Coordinator
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
import datetime

from resources.hash_encrypt import encrypt_val, hash_code_generator
from resources.send_mail import send_mail_with_template

from resources.utility import EmailType as mail_type

from .utility import campus_list, coordinator_name, campus_course_list, batch_id_gen, payment_modes
# ----------------------------------------------


# Campus Registration Models for Campus Students @ Admin Mode
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
    enrollment_id = models.CharField(max_length=32, blank=False, default=None)

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
    payment_mode = models.CharField(_("Modes of payment"), choices=payment_modes(), default=None, max_length=32)
    admission_fees_amount = models.IntegerField(blank=False, default=0)
    fees_status = models.BooleanField(_("Fees Status (Tick if Paid)"), blank=False, default=False)
    transaction_id = models.CharField(_("Enter the Transaction id (Cash memo number for Cash Mode)"), max_length=234, blank=False, default=None)

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
