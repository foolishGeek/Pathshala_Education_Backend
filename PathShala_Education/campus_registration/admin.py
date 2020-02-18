from django.contrib import admin
from .models import CampusRegistration, RegisteredCourse
from django.contrib.auth.models import Group, User
from django.contrib.admin.models import LogEntry


# Make the admin class for the respective models here

# TODO: Model Class ->  :: REGISTER COURSE INLINE ::

class RegisterCourseInline(admin.TabularInline):
    model = RegisteredCourse
    extra = 1
    fields = ('student_id', 'course_id', 'course_activation_id', 'batch_id')
    readonly_fields = ['batch_id', 'course_activation_id', ]
    can_delete = False


# TODO: Model Class ->  :: REGISTER COURSE ADMIN ::

class RegisterCourseAdmin(admin.ModelAdmin):
    model = RegisteredCourse
    fields = ('student_id', 'course_id', 'course_activation_id', 'batch_id')
    readonly_fields = ['batch_id', 'course_activation_id', ]
    list_display = ['student_id', 'course_id', 'batch_id']
    search_fields = ['student_id', 'batch_id']


# TODO: Model Class ->  :: CAMPUS CLASS ::

class CampusRegistrationAdmin(admin.ModelAdmin):
    model = CampusRegistration
    inlines = (RegisterCourseInline,)
    readonly_fields = ['is_registered_app', 'coordinator_name']
    list_display = ['username', 'first_name', 'last_name', 'email_id', 'mobile_no']
    search_fields = ['mobile_no', 'username', 'first_name', 'email']
    list_display_links = ['username', 'first_name', 'last_name', 'email_id', 'mobile_no']


admin.site.register(CampusRegistration, CampusRegistrationAdmin)
admin.site.register(RegisteredCourse, RegisterCourseAdmin)

# MARK: Removed the User & Groups method and Other Clean up
LogEntry.objects.all().delete()
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.disable_action('delete_selected')
