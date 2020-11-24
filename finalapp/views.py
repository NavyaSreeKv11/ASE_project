from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import os

from .models import Document
from .forms import DocumentForm
def home(request):
    return render(request, 'finalapp/home.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            formInstance = form.save(commit=False)
            formInstance.user = request.user

            formInstance.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'finalapp/model_form_upload.html', {
        'form': form
    })
def searchdata(request):
     if request.method=="GET":
         key=request.GET.get('searchword')
         #key2=request.GET.get('searchwordmain')
         searchedlist=Document.objects.filter(Q(category__icontains=key) | Q(name__icontains = key))
         #print(searcheddict)
         #x = Document.objects.filter(category__icontains=key)
         #print(x)
         #z = {**x,**searcheddict}
         #print(z)
         # if len(searcheddict)==0:
         #     searcheddict=Document.objects.filter(category__icontains=key)
         #searcheddict2=Document.objects.filter(name__icontains=key)
         #searcheddict2=Document.objects.filter(name__icontains=key2)
         items=[]

         #searchedlist=[]
         # for obj in queryset:
         #     if obj.name==key:
         #         print(obj.name)
         #for p in Document.objects.raw("SELECT * FROM finalapp_Document WHERE name LIKE key"):
         #  searchedlist.append(p)
         #  print(p.name)
         #print(settings.MEDIA_DIR)
         #for p in searcheddict:

            # x = str(p.image)
            # y = os.path.join(settings.MEDIA_DIR,x)
            #print(y)
            #listimages.append(y)
            #listimages.append(y)
            #print("df",listimages)
         #listimages = [w.replace('\\', '\') for w in listimages]
         #print(listimages)
         context={'items':searchedlist}

     return render(request,'myapp/category/index.html',context)

# Create your views here.
