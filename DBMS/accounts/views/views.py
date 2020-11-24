import time

from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.views.generic import FormView,View,ListView
from django.shortcuts import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse

from accounts.models import File
from accounts.forms import FileForm

from accounts.models import EmailActivation
from accounts.forms import LoginForm, EditProfileForm
from events.models import borrower_detail
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.safestring import mark_safe

class AccountEmailActivateView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(request, "Your email has been confirmed. Please login.")
            return redirect("login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = """Your email has already been confirmed
                Do you need to <a href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("login")
        return render(request, 'registration/activation-error.html', {})

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        pass



class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = "/"

    def form_valid(self, form):
        request = self.request
        #for advance redirecction
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        return super(LoginView, self).form_invalid(form)





def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html',args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST , request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


class ProgressBarUploadView(View):
    def get(self, request):
        if request.user.is_teacher:
            file_list = File.objects.filter(teacher=request.user)
            return render(self.request, 'accounts/slides/base.html', {'files': file_list})
        else:
            return redirect('/')
    def post(self, request):
        if request.user.is_teacher:
            time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
            form = FileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                file = form.save(commit=False)
                file.teacher=request.user
                file.save()

                data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)
        else:
            return redirect('/')



def clear_database(request):

    for file in File.objects.filter(teacher=request.user):
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))


class borrowed_books(LoginRequiredMixin,ListView):
    template_name = 'accounts/borrowed_book.html'
    context_object_name = 'books'
    def get_queryset(self):
        #Notification.objects.mark_all_as_read(recipient = self.request.user)
        return borrower_detail.objects.filter(name = self.request.user)
