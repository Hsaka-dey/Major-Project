from django.db import models
import os
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class BaseUserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, name, password, **extra_fields)

class user(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    subject = models.CharField(max_length=80)
    semester = models.CharField(max_length=10)

    def __str__(self):
        return self.subject


class SessionYear(models.Model):
    session = models.CharField(max_length=10)

    def __str__(self):
        return self.session


class SemToYear(models.Model):
    semester = models.CharField(max_length=10)
    year = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.year} year {self.semester} sem'


class Department(models.Model):
    department = models.CharField(max_length=3)

    def __str__(self):
        return self.department


class Student(models.Model):

    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        filename = '{}.{}'.format(instance.RegID, ext)
        
        # return the whole path to the file
        return os.path.join("Student", filename)
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    RegID = models.CharField(max_length=10)
    Photo = models.FileField(upload_to=wrapper)
    Name = models.CharField(max_length=50)
    DOB = models.DateField()
    Gender = models.CharField(max_length=10)
    Major = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    Sem = models.ForeignKey(SemToYear, on_delete=models.SET_NULL, null=True)
    Phone = models.IntegerField()
    Email = models.EmailField(max_length=100)
    # attendance = models.ForeignKey(Attendance, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.Major} {self.RegID} {self.Name}"
    
