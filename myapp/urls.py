from django.urls import path
from myapp import views


app_name='myapp'

urlpatterns=[
     path('index/(?P<value>\s+)',views.index,name='index'),
    path('category',views.category,name='category')

]
