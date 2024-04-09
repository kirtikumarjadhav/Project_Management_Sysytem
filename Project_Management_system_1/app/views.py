from typing import Any
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Project
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project
from django.contrib.auth.decorators import login_required


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        
        return reverse_lazy('project_create')


class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('project_create')  
    def form_valid(self, form):
        user = form.save()
       
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('project_create')  
        return super(RegisterPage, self).get(*args, **kwargs)

@login_required
def project_create(request):
    if request.method == 'POST':
       
        project_name = request.POST.get('project_name')
        reason = request.POST.get('reason')
        type = request.POST.get('type')
        division = request.POST.get('division')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        department = request.POST.get('department')
        location = request.POST.get('location')
       
        start_date = parse_date(request.POST.get('start_date'))
        end_date = parse_date(request.POST.get('end_date'))
        status = request.POST.get('status', 'registered')
        

        project = Project(

            project_name=project_name,
            reason=reason,
            type=type,
            division=division,
            category=category,
            priority=priority,
            department=department,
            location=location,
            start_date=start_date,
            end_date=end_date,
            status=status 
        )

       
        if start_date and end_date and end_date < start_date:
            return HttpResponse("End date cannot be earlier than the start date.", status=400)
        
        try:
            project.user = request.user 
            project.full_clean()
            project.save()
           
            return redirect('project_success')
        except ValidationError as e:
            return HttpResponse(f"Error: {e.message_dict}", status=400)
    
    
    return render(request, 'add_project.html', {})




def project_success(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    project_list = Project.objects.filter(user=request.user)  
    paginator = Paginator(project_list, 10)  
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    return render(request, 'success.html', {'projects': projects})


@require_POST
def update_status_start(request, project_id):
    return update_status(request, project_id, 'Running')

@require_POST
def update_status_close(request, project_id):
    return update_status(request, project_id, 'Closed')

@require_POST
def update_status_cancel(request, project_id):
    return update_status(request, project_id, 'Cancelled')

def update_status(request, project_id, new_status):
    try:
        project = Project.objects.get(id=project_id)
        project.status = new_status
        project.save()
        return JsonResponse({'status': 'success', 'new_status': new_status})
    except Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found.'}, status=404)

@require_POST
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({'status': 'success', 'message': 'Project deleted successfully'})
    except Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)

from django.utils import timezone
from django.http import JsonResponse
from .models import Project

def dashboard_counters(request):
    total_projects = Project.objects.count()
    closed_projects = Project.objects.filter(status='Closed').count()
    running_projects = Project.objects.filter(status='Running').count()
    cancelled_projects = Project.objects.filter(status='Cancelled').count()
    closure_delay_projects = Project.objects.filter(status='Running', end_date__lt=timezone.now()).count()

    data = {
        'total_projects': total_projects,
        'closed_projects': closed_projects,
        'running_projects': running_projects,
        'cancelled_projects': cancelled_projects,
        'closure_delay_projects': closure_delay_projects,
    }
    return JsonResponse(data)

from django.shortcuts import render
from .models import Project
from django.db.models import Count

from django.shortcuts import render
from django.db.models import Count, Q
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Project
from django.core.serializers import serialize
from django.utils.safestring import mark_safe

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    status_counts = list(Project.objects.filter(user=request.user).values('status').annotate(count=Count('status')))
    department_data = list(Project.objects.filter(user=request.user).values('department').annotate(
        total=Count('id'),
        closed=Count('id', filter=Q(status='Closed'))
    ))

    status_counts_json = mark_safe(json.dumps(status_counts, cls=DjangoJSONEncoder))
    department_data_json = mark_safe(json.dumps(department_data, cls=DjangoJSONEncoder))

    return render(request, 'dashboard.html', {
        'status_counts_json': status_counts_json,
        'department_data_json': department_data_json,
    })

