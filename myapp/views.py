from django.shortcuts import render
from finalapp.models import Document
import os
from django.conf import settings

# Create your views here.
#import pathlib
def index(request,value):
    p=Document.objects.filter(category=value)
    items=[]
    listitems=[]
    # for w in p:
    #     if w.category=='Animals':
    #         x=str(w.image)
    #         #print(settings.MEDIA_DIR)
    #         pathimage=os.path.join(settings.MEDIA_DIR,x)
    #         #pathimage=pathlib.PureWindowsPath(pathimage)
    #         #print(pathimage.as_posix())
    #         #print(pathimage)
    #         items.append(pathimage)
    #         listitems=[w.replace('\\','/') for w in items]
    #
    # print(listitems)
    #     # for i in items:
    #     #     i.replace("''\'","/")
    #     #print(items)
    # list1=['C:/Users/ramya sahitya/Documents/GitHub/ase_project/media/animal1.jpg','C:/Users/ramya sahitya/Documents/GitHub/ase_project/media/animal1_apsFEQL.jpg','C:/Users/ramya sahitya/Documents/GitHub/ase_project/media/animal2.jpg','C:/Users/ramya sahitya/Documents/GitHub/ase_project/media/animal2_vgxt2YQ.jpg']
    # items=['../static/category/images/1.jpg','../static/category/images/2.jpg']
    context={'items':p}
    return render(request, 'myapp/category/index.html', context)


def category(request):
    return render(request,'myapp/category/category.html')
