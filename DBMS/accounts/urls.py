
from django.urls import path,re_path
from django.conf.urls import url

from .views import home1

from .views import views
from .views.students import StudentSignup
from .views.teachers import TeacherSignup
from .views.general import GeneralSignup
urlpatterns = [

    #path('', home1.home, name='home'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
            views.AccountEmailActivateView.as_view(),
            name='email-activate'),
    path('studentsignup/', StudentSignup, name="student_signup_new"),
    path('teachersignup/', TeacherSignup, name="teacher_signup_new"),
    path('generalsignup/', GeneralSignup, name="general_signup_new"),

    path('signup/', home1.SignUpView.as_view(),name="signup_all"),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    path('borrowed-books/', views.borrowed_books.as_view(), name='borrowed_books'),

]
