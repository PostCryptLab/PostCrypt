from django.shortcuts import redirect, render, get_object_or_404
from .models import Document, LabChoice
from .forms import DocumentForm, LabChoiceForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from nbconvert import HTMLExporter
import nbformat

# import myproject.settings
from pathlib import Path
import subprocess
import os

def home(request):
    # Document.objects.all().delete()
    context = {'form': DocumentForm()}
    return render(request, 'list.html', context)

@login_required # type: ignore
def courses_view(request):
    documents = Document.objects.all()
    context = {
        'documents': documents, 
        'form': DocumentForm(),
        'user': request.user,
        'lab_choice_form': LabChoiceForm()
        }
    return render(request, 'dashboard.html', context)

def my_results_view(request):

    lab_tester_script_path = os.path.join(settings.BASE_DIR, 'scripts', 'TestSystem', 'labTester.py')
    lab_path = os.path.join(settings.MEDIA_ROOT, 'labs', request.GET['labName'])

    print("Result view")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['docfile']
            newdoc = Document(docfile=file)

            newdoc.lab_type = request.POST['labName']

            newdoc.save()

            proc = subprocess.run(["python3", lab_tester_script_path,
                                   newdoc.docfile.path], universal_newlines=False,
                                  stdout=subprocess.PIPE, encoding="utf-8")

            context = {'response': proc.stdout.splitlines()}
            return render(request, 'results.html', context)

    if request.method == 'GET':
        print(request.GET)
        proc = subprocess.run(["python3", lab_tester_script_path, lab_path], 
                              universal_newlines=False,
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

@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    with document.docfile.open('rb') as f:
        notebook_content = f.read().decode('utf-8')
    
    notebook_node = nbformat.reads(notebook_content, as_version=4)
    
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    body, _ = html_exporter.from_notebook_node(notebook_node)
    
    return HttpResponse(body, content_type='text/html')

@login_required
def create_lab(request):
    if request.method == 'POST':
        form = LabChoiceForm(request.POST)
        if form.is_valid():
            # Create a new LabChoice instance and save it
            LabChoice.objects.create(name=form.cleaned_data['labname'])
            return redirect('dashboard')  # Redirect to a relevant page, like 'dashboard'
    else:
        form = LabChoiceForm()
    return render(request, 'dashboard.html', {'lab_choice_form': form})