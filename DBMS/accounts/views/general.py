
from django.shortcuts import redirect, render

from ..forms import  generalSignUpForm,GeneralExtraForm
from ..models import User


def GeneralSignup(request):
    if request.method == "POST":
        form1 = generalSignUpForm(request.POST or None)
        form2 = GeneralExtraForm(request.POST or None)
        if form1.is_valid() and form2.is_valid():
            ins = form1.save(commit=False)
            ins.is_general = True
            ins.is_active = False
            ins.save()

            email = ins.email
            model_instance = form2.save(commit=False)
            user = User.objects.get(email=email)
            model_instance.user =user
            model_instance.save()
            return redirect('/')
    else:
        print("form is invalid")

        form1 = generalSignUpForm()
        form2 = GeneralExtraForm()
    return render(request,'accounts/student_signup.html',{"form1":form1,"form2":form2})












