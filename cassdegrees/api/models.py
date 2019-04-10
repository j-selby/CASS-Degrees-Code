from django.db import models


class SampleModel(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    text = models.CharField(max_length=100)


class CourseModel(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    units = models.PositiveIntegerField()
    offeredSem1 = models.BooleanField()
    offeredSem2 = models.BooleanField()

    class Meta:
        unique_together = (("code", "year"),)


class CoursesInSubplanModel(models.Model):
    subplanId = models.ForeignKey('SubplanModel', on_delete=models.CASCADE)
    courseId = models.ForeignKey('CourseModel', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("subplanId", "courseId"),)


class SubplanModel(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    year = models.PositiveIntegerField()
    name = models.CharField(max_length=256)
    units = models.PositiveIntegerField()

    major = "MAJ"
    minor = "MIN"
    specialisation = "SPEC"
    subplanChoices = ((major, "Major"), (minor, "Minor"), (specialisation, "Specialisation"))

    planType = models.CharField(max_length=4, choices=subplanChoices)
    courses = models.ManyToManyField(CourseModel, through=CoursesInSubplanModel)

    class Meta:
        unique_together = (("code", "year"),)
