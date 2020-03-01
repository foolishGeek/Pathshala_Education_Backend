from django.core.mail import EmailMultiAlternatives, send_mail
from .hash_encrypt import decrypt_val
from django.template.loader import get_template


# TODO : Make the Send mail with Template function:

def send_mail_with_template(mail_type, kargs):
    print("course_detail_act_code", kargs['course_activation_id'])
    print(mail_type.REGISTRATION.value)
    mail_to_address = kargs['email_id']
    subject_string = "Course Activation Message"
    message_body = "Hi {}, \nThank you for registering with the {} course.\nHappy Learning! Please find the " \
                   "secret activation code below for app registration. \n*Please Keep the code secret. \nCourse " \
                   "Activation ID: {}".format(
        kargs['first_name'] + " " + kargs['last_name'], kargs['course_name'],
        decrypt_val(kargs['course_activation_id']))
    reg_course_template = get_template('mail.html')
    context = {'username': kargs['username'], 'course_name': kargs['course_name'],
               'batch_id': kargs['batch_id'],
               'course_activation_id': decrypt_val(kargs['course_activation_id'])}
    temp = reg_course_template.render(context)
    msg = EmailMultiAlternatives(subject_string, message_body, 'avijitgoswami72@gmail.com', [mail_to_address])
    msg.attach_alternative(temp, 'text/html')
    msg.send()


# TODO : Send text mail to user

def send_mail_to_user():
    pass
