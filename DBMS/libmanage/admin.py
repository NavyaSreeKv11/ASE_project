from django.contrib import admin

# Register your models here.
from .models import Fullname,Student,Course

admin.site.register(Fullname)
admin.site.register(Student)
admin.site.register(Course)