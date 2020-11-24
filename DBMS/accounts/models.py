from datetime import timedelta

from django.conf import settings
from django.urls import reverse

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager
)
from django.template.loader import get_template
from django.utils import timezone

from book.models import Book

from bookcafe.utils import unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)




class UserManager(BaseUserManager):
    def create_user(self,email,first_name=None,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("users must have email address")
        if not password:
            raise ValueError("users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name=first_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active= is_active
        user_obj.is_active= is_active
        user_obj.admin = is_admin

        user_obj.save(using=self._db)
        return user_obj

    # def create_stffuser
    def create_staffuser(self,email,first_name=None,password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self,email,first_name=None,password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
            is_staff=True,
            is_admin=True
        )



class User(AbstractBaseUser):
    username = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(unique=True,max_length=255)
    first_name   = models.CharField(max_length=255, blank=True, null=True)
    last_name   = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    book_issued = models.ManyToManyField(Book,blank=True)
    is_student = models.BooleanField(default=False)
    is_general = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    phone_no=models.IntegerField(blank=True, null=True)
    bio=models.TextField(max_length=255, blank=True, null=True)
    image=models.ImageField(upload_to='profile_image',blank=True, null=True)



    USERNAME_FIELD = 'email'
    #email and password field are required by default

    REQUIRED_FIELDS = []


    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True


    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    # @property
    # def is_active(self):
    #     return  self.active
    def testinguser(self):
        return '%s, %s, %s' % (self.first_name, self.last_name,self.email)
class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
              ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
              )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

class EmailActivation(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()  # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False


    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'python')
                key_path = reverse("accounts:email-activate", kwargs={'key': self.key}) # use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently=False,
                    )
                return sent_mail
        return False



def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=User)


class File(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    file = models.FileField(upload_to='media_/files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)









































class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #dob = models.DateField(null=True,blank=True)
    bio  =models.TextField(null=True,blank=True)
    college = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return str(self.user.email)


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    

class General(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.IntegerField(null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    city = models.CharField(max_length=255)
