from django.db import models
from django.contrib.auth.models import User
from student.models import StudentProfile

class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_kumpulan = models.ManyToManyField('student.kumpulan', blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
class Lecturer(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class ClassMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='class_materials/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title