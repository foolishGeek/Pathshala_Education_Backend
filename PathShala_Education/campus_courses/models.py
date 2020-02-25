from django.db import models


# TODO: Create the courses that are available for the campus students.
#   ==================== :: SCHEMA :: =====================
#   - Course_id
#   - course_name
#   - course_duration
#   - initial_payment
#   - recurring_payment
#   - batch_id


class CampusCourse(models.Model):
    course_id = models.CharField(max_length=64, blank=False, default=None)
    course_name = models.CharField(max_length=128, blank=False, default=None)
    course_duration = models.IntegerField(blank=False, default=0)
    initial_payment = models.IntegerField(blank=False, default=0)
    recurring_payment = models.IntegerField(blank=False, default=0)
    batch_size = models.IntegerField(blank=False, default=0)

    def save(self, *args, **kwargs):
        self.course_id = self.course_id.upper()
        super(CampusCourse, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name
