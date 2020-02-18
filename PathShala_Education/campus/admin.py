from django.contrib import admin
from .models import Coordinator, Campus



class CoordinatorAdmin(admin.ModelAdmin):
    model = Coordinator


class CampusAdmin(admin.ModelAdmin):
    model = Campus
    list_display = ['campus_name', 'campus_code']
    list_display_links = []


admin.site.register(Campus, CampusAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
