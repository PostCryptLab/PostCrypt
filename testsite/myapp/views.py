from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# import myproject.settings
from pathlib import Path
import subprocess
import os

def my_view(request):
    documents = Document.objects.all()
    # Document.objects.all().delete()
    context = {'documents': documents, 'form': DocumentForm()}
    return render(request, 'list.html', context)

@login_required # type: ignore
def courses_view(request):
    documents = Document.objects.all()
    context = {
        'documents': documents, 
        'form': DocumentForm(),
        'user': request.user
        }
    return render(request, 'dashboard.html', context)

def my_results_view(request):
    print("Result view")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['docfile']
            newdoc = Document(docfile=file)

            newdoc.lab_type = request.POST['labName']

            newdoc.save()

            proc = subprocess.run(["python3", r"C:\Users\ivanz\uni\Inż\PostCrypt\TestSystem\main.py",
                                   newdoc.docfile.path], universal_newlines=False,
                                  stdout=subprocess.PIPE, encoding="utf-8")

            context = {'response': proc.stdout.splitlines()}
            return render(request, 'results.html', context)

    if request.method == 'GET':
        print(request.GET)
        proc = subprocess.run(["python3", r"C:\Users\ivanz\uni\Inż\PostCrypt\TestSystem\main.py",
                               r"C:\Users\ivanz\uni\Inż\PostCrypt\testsite\media\labs\{}".format(request.GET['labName'])], universal_newlines=False,
                              stdout=subprocess.PIPE, encoding="utf-8")

        # for text_line in proc.stdout.splitlines():
        #     print(text_line)

        context = {'response': proc.stdout.splitlines()}
        return render(request, 'results.html', context)



class MyLoginView(LoginView):
    template_name = 'templates/login.html' 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('my-view') 
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})