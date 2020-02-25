from django.contrib import admin
from .models import CampusCourse


class CampusCourseAdmin(admin.ModelAdmin):
    model = CampusCourse
    fields = ['course_id', 'course_name', 'course_duration', 'initial_payment', 'recurring_payment', 'batch_size']
    list_display = ['course_id', 'course_name', 'course_duration', 'initial_payment', 'recurring_payment', 'batch_size']
    list_display_links = ['course_id','course_name']
    search_fields = ['course_name', 'course_id']


admin.site.register(CampusCourse, CampusCourseAdmin)
