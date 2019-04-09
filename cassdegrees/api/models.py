from django.db import models


class SampleModel(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    text = models.CharField(max_length=100)


class CourseModel(models.Model):
    code = models.CharField(max_length=32)
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    units = models.PositiveIntegerField()
    offered_sem1 = models.BooleanField()
    offered_sem2 = models.BooleanField()

    class Meta:
        unique_together = (("code", "year"),)


class SubplanModel(models.Model):
    code = models.CharField(max_length=32)
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    units = models.PositiveIntegerField()

    major = "MAJ"
    minor = "MIN"
    specialisation = "SPEC"
    subplan_choices = ((major, "Major"), (minor, "Minor"), (specialisation, "Specialisation"))

    plan_type = models.CharField(max_length = 4, choices=subplan_choices)

    class Meta:
        unique_together = (("code", "year"),)
