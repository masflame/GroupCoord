from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import Task, Project

@csrf_exempt  # Temporarily disable CSRF for debugging (remove this in production)
def delete_task(request, task_id):
    """
    Deletes a task.
    """
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()  # Permanently removes the task from the database
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def edit_task(request, task_id):
    """
    Edits a task's details.
    """
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.title = request.POST.get('title')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.due_date = request.POST.get('due_date')
        task.save()
        return JsonResponse({'success': True, 'assigned_to': task.assigned_to.username})
    return JsonResponse({'success': False}, status=400)

def dashboard(request):
    projects = Project.objects.all()
    created_projects = projects.filter(created_by=request.user).count()
    invited_projects = projects.exclude(created_by=request.user).filter(members=request.user).count()
    total_projects = created_projects + invited_projects

    context = {
        'projects': projects,
        'created_projects': created_projects,
        'invited_projects': invited_projects,
        'total_projects': total_projects,
    }
    return render(request, 'dashboard.html', context)
