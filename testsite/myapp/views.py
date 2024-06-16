from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
import subprocess
import os

def my_view(request):
    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    # else:
    #     form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page

    documents = Document.objects.all()
    # print(documents)

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': DocumentForm(), 'message': message}
    return render(request, 'list.html', context)


def my_results_view(request):
    print("Result view")
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # print(newdoc.docfile.name)
            proc = subprocess.run(["python3", r"C:\Users\ivanz\uni\Inż\PostCrypt\TestSystem\main.py",
                            r"C:\Users\ivanz\uni\Inż\PostCrypt\testsite\media\labs\lab1"], universal_newlines=False,
                                  stdout=subprocess.PIPE, encoding="utf-8")
            for text_line in proc.stdout.splitlines():
                print(text_line)

            # print(doc.stdout)
            # os.system(r"python3 C:\Users\ivanz\uni\Inż\PostCrypt\TestSystem\main.py " + str(newdoc.docfile.name))

            # Redirect to the document list after POST
            return redirect('my-view')
        # else:
        #     message = 'The form is not valid. Fix the following error:'
    # else:
    #     form = DocumentForm()  # An empty, unbound form
    # pass