from django.db import models


# TODO: This is CAMPUS Model:
#  ========================================
#  Schema:
#  ----------------------------------------
#  - name
#  - code
#  - coordinator - related field


class Campus(models.Model):
    campus_name = models.CharField(max_length=64, blank=False, default=None)
    campus_code = models.CharField(max_length=20, blank=False, default=None)

    def __str__(self):
        return self.campus_name


# TODO: This is CAMPUS_COORDINATOR Model:
#  ========================================
#  Schema:
#  ----------------------------------------
#  - name
#  - TODO Create a filed that store the campus


class Coordinator(models.Model):
    name = models.CharField(max_length=64, blank=False, default=None)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="coordinators", default=None)

    def __str__(self):
        return self.name

