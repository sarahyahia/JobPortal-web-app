from django.db import models
from django.contrib.auth.models import User


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=254)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


EXPERIENCE_CHOICES = [
    ("Junior","Jr"),
    ( "Mid", "Mid"),
    ("Senior","Sr" )
]

class Employee(models.Model):
    user = models.OneToOneField(User,primary_key = True,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    nationalID = models.CharField(max_length=14, unique=True, error_messages={'invalid':"National Id is already exist!"})
    city = models.CharField(max_length=100,null= True)
    email = models.EmailField( max_length=254)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES,null= True)
    little_bio = models.TextField()
    programming_language=models.ManyToManyField(ProgrammingLanguage)
    views = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)

JOB_STATUS_CHOICES =[
    (0,'Open'),
    (1,'Closed')
]

class Job(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=254)
    city = models.CharField(max_length=100)
    job_status = models.IntegerField(choices=JOB_STATUS_CHOICES)
    programming_language=models.ManyToManyField(ProgrammingLanguage)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    def __str__(self):
        return str( self.job_title)

# class Employer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     company = models.CharField( max_length=50,null=True)


STATUS_CHOICES=[
    (0,'Review'),
    (1,'Accepted'),
    (2, 'Rejected')
]

class JobApplicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    applicant_status = models.IntegerField( choices=STATUS_CHOICES, default='Review')
    def __str__(self):
        return str( self.job.job_title+ ' applicant ' + self.applicant.name)