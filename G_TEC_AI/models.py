from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField()  # "HTML,CSS,JS"
    level = models.CharField(max_length=50)  # Beginner/Intermediate
    duration = models.CharField(max_length=50)

