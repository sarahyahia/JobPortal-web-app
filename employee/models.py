from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email.')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    date_joined = models.DateField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateField(_("last login"), auto_now=True, null = True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    isEmployer = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Employer(models.Model):
    user = models.OneToOneField(User, related_name='EmployerProfile', on_delete=models.CASCADE)
    company = models.CharField( max_length=50,null=True)

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=254)
    isActive = models.BooleanField(default=False)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

EXPERIENCE_CHOICES = [
    ("Junior","Jr"),
    ( "Mid", "Mid"),
    ("Senior","Sr" )
]

class Employee(models.Model):
    user = models.OneToOneField(User, related_name='EmployeeProfile',primary_key = True,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, blank=True)
    nationalID = models.CharField(max_length=14, unique=True, error_messages={'invalid':"National Id is already exist!"})
    city = models.CharField(max_length=100,null= True)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES,null= True)
    little_bio = models.TextField()
    programming_language=models.ForeignKey(ProgrammingLanguage, verbose_name=_("programming languages"), on_delete=models.DO_NOTHING)
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
    programming_language=models.ForeignKey(ProgrammingLanguage, verbose_name=_("programming languages"), on_delete=models.DO_NOTHING)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    def __str__(self):
        return str( self.job_title)



STATUS_CHOICES=[
    (0,'Review'),
    (1,'Accepted'),
    (2, 'Rejected')
]

class JobApplicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    applicant_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Review')
    def __str__(self):
        return str( self.job.job_title)
    def __iter__(self):
        return [ self.job, self.applicant, self.applicant_status]