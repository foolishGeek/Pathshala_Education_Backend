from campus_courses.models import CampusCourse
from campus.models import Coordinator, Campus


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
    print("Campus List*******************")
    print(lists)
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



# This field return tuple for the payment mode in campus stduent admission:

def payment_modes():

    modes = [
        ("CSH", "CASH"),
        ("GPAY", "GOOGLE PAY"),
        ("PayTM", "PAYTM")
    ]
    return modes
