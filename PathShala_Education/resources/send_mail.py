from django.core.mail import EmailMultiAlternatives, send_mail

from .utility import decrypt_val
from django.template.loader import get_template


# TODO : Make the Send mail with Template function:

def send_mail_with_template(course_detail):
    print("course_detail_act_code", course_detail['course_activation_id'])
    mail_to_address = course_detail['email_id']
    subject_string = "Course Activation Message"
    message_body = "Hi {}, \nThank you for registering with the {} course.\nHappy Learning! Please find the " \
                   "secret activation code below for app registration. \n*Please Keep the code secret. \nCourse " \
                   "Activation ID: {}".format(
        course_detail['first_name'] + " " + course_detail['last_name'], course_detail['course_name'],
        decrypt_val(course_detail['course_activation_id']))
    reg_course_template = get_template('mail.html')
    context = {'username': course_detail['username'], 'course_name': course_detail['course_name'],
               'batch_id': course_detail['batch_id'],
               'course_activation_id': decrypt_val(course_detail['course_activation_id'])}
    temp = reg_course_template.render(context)
    msg = EmailMultiAlternatives(subject_string, message_body, 'avijitgoswami72@gmail.com', [mail_to_address])
    msg.attach_alternative(temp, 'text/html')
    msg.send()


# TODO : Send text mail to user

def send_mail_to_user():
    pass
