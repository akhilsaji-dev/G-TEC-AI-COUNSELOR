from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField()  # "HTML,CSS,JS"
    level = models.CharField(max_length=50)  # Beginner/Intermediate
    duration = models.CharField(max_length=50)


class ChatHistory(models.Model):
    user_input = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)