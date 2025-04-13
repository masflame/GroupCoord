from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Project, Task, FileUpload
from .forms import ProjectForm, TaskForm, FileUploadForm
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful! You are now logged in.")
                return redirect('dashboard')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()

            # Handle members manually
            members_data = request.POST.get('members_data', '[]')  # Get the JSON string of emails
            try:
                email_list = json.loads(members_data)  # Parse the JSON string into a Python list
                for email in email_list:
                    try:
                        user = User.objects.get(email=email)  # Find the user by email
                        project.members.add(user)  # Add the user to the project's members
                    except User.DoesNotExist:
                        continue  # Skip if the user does not exist
            except json.JSONDecodeError:
                pass  # Handle invalid JSON silently

            # Add the current user to the project members
            project.members.add(request.user)

            return redirect('dashboard')  # Refresh the page after saving
    else:
        form = ProjectForm()

    # Fetch projects where the user is a member
    projects = Project.objects.filter(members=request.user)

    # Calculate progress for each project
    for project in projects:
        project.calculate_progress()

    return render(request, 'dashboard.html', {'projects': projects, 'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    files = FileUpload.objects.filter(project=project)

    # Initialize forms
    task_form = TaskForm(project=project)
    file_form = FileUploadForm()

    if request.method == 'POST':
        if 'task_submit' in request.POST:
            task_form = TaskForm(request.POST, project=project)  # Pass the project
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.project = project
                task.save()
                project.calculate_progress()  # Update progress after adding a task
                return redirect('project_detail', project_id=project.id)  # Redirect to clear the form
        elif 'file_submit' in request.POST:
            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                upload = file_form.save(commit=False)
                upload.project = project
                upload.uploaded_by = request.user
                upload.save()
        elif 'invite_member_submit' in request.POST:
            members_data = request.POST.get('members_data', '[]')  # Get the JSON string of emails
            try:
                email_list = json.loads(members_data)  # Parse the JSON string into a Python list
                for email in email_list:
                    try:
                        user = User.objects.get(email=email)  # Find the user by email
                        project.members.add(user)  # Add the user to the project's members
                    except User.DoesNotExist:
                        continue  # Skip if the user does not exist
            except json.JSONDecodeError:
                pass  # Handle invalid JSON silently

    progress = project.progress

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'files': files,
        'task_form': task_form,
        'file_form': file_form,
        'progress': int(progress),
        'project_members': project.members.all()
    })