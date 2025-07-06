from django.db import models
from django.contrib.auth.models import User

class Kumpulan(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kumpulan = models.ForeignKey(Kumpulan, on_delete=models.SET_NULL, null=True)
    program = models.CharField(max_length=20)
    kod_kursus = models.CharField(max_length=20)
    no_pelajar = models.CharField(max_length=20)
    nama = models.CharField(max_length=255, default="Muhammad Ali")
    fyp_title = models.CharField(max_length=255)
    profile_picture = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.get_full_name()
    
class Milestone(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
  
    def __str__(self):
        return self.title
    
class Submission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissoins')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='submission/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.timestamp:
            time_str = self.timestamp.strftime('%Y-%m-%d %H:%M')
        else:
            time_str = "unsaved"
        return f"Comment by {self.author.email} on {time_str}"

class SupervisorRequest(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    lecturer = models.ForeignKey('lecturer.LecturerProfile', on_delete=models.CASCADE)
    fyp_title = models.CharField(max_length=255, blank=True)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} + {self.lecturer.user.get_full_name()}"
    