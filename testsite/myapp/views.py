from django.shortcuts import redirect, render, get_object_or_404
from .models import Document, LabChoice, OneTimeCode
from .forms import DocumentForm, LabChoiceForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from nbconvert import HTMLExporter
from django.contrib import messages
import nbformat
from django.core.exceptions import ValidationError
from scripts.TestSystem.master_nb_formatter import format_notebook
from scripts.TestSystem.labTester import LabTester
from django.http import FileResponse
from django.utils.crypto import get_random_string
# import myproject.settings
from pathlib import Path
import subprocess
import os

def home(request):
    # Document.objects.all().delete()
    context = {'form': DocumentForm()}
    return render(request, 'list.html', context)

@login_required
def delete_lab_type(request):
    if request.method == 'POST':
        lab_type_id = request.POST.get('lab_type_id')
        lab_type = get_object_or_404(LabChoice, id=lab_type_id)

        # Delete all documents associated with this lab type
        Document.objects.filter(lab_type=lab_type.name).delete()

        # Delete the lab type itself
        lab_type.delete()

        messages.success(request, f'Lab type "{lab_type.name}" and all associated documents have been deleted.')
        return redirect('dashboard')

    # If not a POST request, redirect to the dashboard
    return redirect('dashboard')

@login_required
def dashboard(request):
    # Get all unique lab types (folders) for the filter dropdown
    folders = Document.objects.values_list('lab_type', flat=True).distinct()

    # Filter documents by selected folder (if any)
    selected_folder = request.GET.get('lab_type')
    if selected_folder:
        documents = Document.objects.filter(lab_type=selected_folder)
    else:
        documents = Document.objects.all()

    # Get all Lab types for the delete Lab type section
    lab_types = LabChoice.objects.all()

    # Generate a one-time code
    one_time_code = get_random_string(10)
    OneTimeCode.objects.create(code=one_time_code, user=request.user)

    context = {
        'documents': documents,
        'folders': folders,
        'selected_folder': selected_folder,
        'lab_types': lab_types,  # Pass Lab types to the template
        'form': DocumentForm(),
        'lab_choice_form': LabChoiceForm(),
        'one_time_code': one_time_code,
    }
    return render(request, 'dashboard.html', context)


@login_required
def delete_lab(request, document_id):
    # Get the document to delete
    document = get_object_or_404(Document, id=document_id)

    # Delete the document
    document.delete()

    # Redirect back to the dashboard
    return redirect('dashboard')

@login_required
def courses_view(request):
    documents = Document.objects.all()
    one_time_code = get_random_string(10)
    OneTimeCode.objects.create(code=one_time_code, user=request.user)

    context = {
        'documents': documents,
        'form': DocumentForm(),
        'user': request.user,
        'lab_choice_form': LabChoiceForm(),
        'one_time_code': one_time_code if one_time_code else None
    }
    return render(request, 'dashboard.html', context)

def my_results_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['docfile']
            newdoc = Document(docfile=file)
            newdoc.lab_type = form.cleaned_data['labName'].name
            newdoc.save()

            # Pass the full path of the file for single file testing
            tester = LabTester(newdoc.docfile.path, None)
            results = tester.run_tests(newdoc.docfile.path),

            context = {
                'results': results,
                'test_summary': tester.get_test_summary(),
                'lab_name': newdoc.lab_type
            }
            return render(request, 'results.html', context)

    if request.method == 'GET':
        lab_name = request.GET.get('labName')
        if not lab_name:
            return HttpResponse("Lab name not provided", status=400)

        lab_dir = os.path.join(settings.LABS_ROOT, lab_name)
        # For directory testing, pass the lab name and directory
        tester = LabTester(lab_name, lab_dir)
        print("Tester args:", lab_name, lab_dir)
        results = tester.run_tests()

        context = {
            'results': results,
            'test_summary': tester.get_test_summary(),
            'lab_name': lab_name
        }
        return render(request, 'results.html', context)



class MyLoginView(LoginView):
    template_name = 'templates/login.html'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
        form = LabChoiceForm(request.POST, request.FILES)
        if form.is_valid():
            lab_name = form.cleaned_data['labname']
            template_file = request.FILES['template_file']

            # Validate file extension
            if not template_file.name.endswith('.ipynb'):
                form.add_error('template_file', 'Only Jupyter notebook (.ipynb) files are allowed.')
                context = {
                    'lab_choice_form': form,
                    'documents': Document.objects.all(),
                    'form': DocumentForm(),
                }
                return render(request, 'dashboard.html', context)

            # Create the lab directory if it doesn't exist
            lab_dir = os.path.join(settings.LABS_ROOT, lab_name)

            print(settings.LABS_ROOT)
            os.makedirs(lab_dir, exist_ok=True)

            # Save the template file temporarily
            temp_path = os.path.join(lab_dir, template_file.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in template_file.chunks():
                    destination.write(chunk)

            try:
                # Format the notebook and get the paths of generated files
                public_path, private_path = format_notebook(temp_path, os.path.join(lab_dir, lab_name))

                # Clean up the temporary file
                os.remove(temp_path)

                # Create a new LabChoice instance and save it
                LabChoice.objects.create(name=lab_name)
                return redirect('dashboard')

            except Exception as e:
                form.add_error('template_file', f'Error processing notebook: {str(e)}')
                # Clean up on error
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        form = LabChoiceForm()

    context = {
        'lab_choice_form': form,
        'documents': Document.objects.all(),
        'form': DocumentForm(),
    }
    return render(request, 'dashboard.html', context)

def download_lab_template(request, lab_name):
    file_path = os.path.join(settings.LABS_ROOT, lab_name, f"{lab_name}_pub.ipynb")
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{lab_name}_pub.ipynb"'
        return response
    return HttpResponse("Template not found", status=404)