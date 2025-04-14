from django.db import models
from django.contrib.auth.models import User
from datetime import date



class Project(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    members = models.ManyToManyField(User)  # Many-to-Many relationship with User
    progress = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def has_notification(self):
        if self.due_date < date.today():
            return True  # Notification for overdue project
        if self.task_set.filter(completed=False).exists():  # Check for incomplete tasks
            return True
        return False

    def calculate_progress(self):
        total_tasks = self.task_set.count()
        if total_tasks == 0:
            self.progress = 0
        else:
            completed_tasks = self.task_set.filter(completed=True).count()
            self.progress = (completed_tasks / total_tasks) * 100
        self.save()

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    

class FileUpload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)