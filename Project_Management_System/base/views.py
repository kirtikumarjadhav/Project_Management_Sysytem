from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def home(request):
 return render(request, "home.html", {})


def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})



from django.shortcuts import render, redirect
from .forms import ProjectForm

from django.shortcuts import render, redirect
from django.contrib import messages  # Import messages
from .forms import ProjectForm



def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been saved successfully!')
            form = ProjectForm()  # Create a new blank form instance
        # If the form is not valid, the same form with errors will be rendered
    else:
        form = ProjectForm()  # Provide a blank form for a GET request

    return render(request, 'add_project.html', {'form': form})



def success_view(request):
    projects = Project.objects.all()
    return render(request, 'success_view.html', {'projects': projects})




