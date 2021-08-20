from django.db import models
from django.contrib.auth.models import User


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.name}"


EXPERIENCE_CHOICES = [
    ("Junior","Junior"),
    ( "Mid", "Mid"),
    ("Senior", "Senior")
]

class Employee(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    nationalID = models.IntegerField()
    city = models.CharField(max_length=100,null= True)
    email = models.EmailField( max_length=254)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES,null= True)
    little_bio = models.TextField()
    programming_language=models.ManyToManyField(ProgrammingLanguage)
    views = models.IntegerField()

    def __str__(self):
        return str(self.name)



class Job(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    job_title = models.CharField(max_length=254)
    city = models.CharField(max_length=100,null= True)
    programming_language=models.ManyToManyField(ProgrammingLanguage)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES,null= True)

    def __str__(self):
        return str( self.job_title)

