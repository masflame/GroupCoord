from django import forms
from .models import Project, Task, FileUpload

# The ProjectForm doesn't handle members directly anymore
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'due_date']  # Removed 'members' field
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # This will render a date picker for the due date
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # This will render a date picker for the due date
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Retrieve the project from kwargs
        super().__init__(*args, **kwargs)
        
        # If a project is provided, filter members for the 'assigned_to' field
        if project:
            self.fields['assigned_to'].queryset = project.members.all()  # Set queryset to project members

# FileUploadForm remains as is, handling file uploads
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
