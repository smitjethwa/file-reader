from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth # type: ignore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd

from .models import Document
from .forms import DocumentForm

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Credentials are Invalid, use admin, admin.', extra_tags='login')
            return redirect('index')

    else:
        return render(request, 'index')

@login_required(login_url='index')
def dashboard(request):
    documents = Document.objects.all()
    context = {
        'documents' : documents
    }
    return render(request, 'dashboard.html', context=context)


def index(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File has been submitted successfully.', extra_tags='file')
            return redirect('index')
    else:
        form = DocumentForm()
    context = {
        'form' : form
    }
    return render(request, 'index.html', context=context)

@login_required(login_url='index')
def logout(request):
    auth.logout(request)
    return redirect('index')

def process_csv(file_name):
    csv_fp = f'media/{file_name}'
    df = pd.read_csv(csv_fp,encoding= 'unicode_escape')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    html_string = f'''
<html>
    <head><title>{file_name.split('.')[0]}</title></head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <body>
    {{table}}
    </body>
</html>.
''' 
    with open('templates/file.html','w', encoding='utf8') as f:
        f.write(html_string.format(table=df.to_html(classes='container pt-4 table table-hover table-bordered',justify='start', index=False).replace('<th>','<th style ="background-color: #cfe2ff; color: black">'))) 


def process_excel(file_name):
    xlsx_fp = f'media/{file_name}'
    read_file = pd.read_excel(xlsx_fp, engine='openpyxl')
    read_file.to_csv(f"media/{file_name.split('.')[0]}.csv",header=True, index=False, errors='ignore', encoding='utf-8')
    process_csv(f"{file_name.split('.')[0]}.csv")


@login_required(login_url='index')
def readfile(request, id):
    document = Document.objects.filter(id=id).values()
    file_name = document[0]['file']
    extension = file_name.split('.')[1]
    if extension == 'csv':
        process_csv(file_name)
    elif extension == 'xlsx':
        process_excel(file_name)
    else:
        return redirect('dashboard')
    context  = {
        'name' : file_name.capitalize().split('.')[0],
        'extension' : extension,
        'path' : file_name
    }
    return render(request, 'data.html', context=context)

