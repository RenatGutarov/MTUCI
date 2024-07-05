from django.db import models

class Resume(models.Model):
    title = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    skills = models.TextField()

    def __str__(self):
        return self.title

