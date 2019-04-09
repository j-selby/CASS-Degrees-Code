from django.db import models


class SampleModel(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    text = models.CharField(max_length=100)

class databaseModel_courses(models.Model):
    code = models.CharField(max_length=32)
    year = models.PositiveIntegerField()
    offered_sem1 = models.BooleanField()
    offered_sem2 = models.BooleanField()

    class Meta:
        unique_together = (("code", "year"),)
