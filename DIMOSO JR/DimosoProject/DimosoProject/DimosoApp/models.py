from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone



class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    

        
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"44.jpg"}'
def get_default_profile_image():
    return "media/44.jpg"

class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone", max_length=15)
    profile_image = models.ImageField(upload_to='get_profile_image_filepath', blank=True, null=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True





class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    
    slug=models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    numbers=models.IntegerField(default=False, blank=True, null=True)
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def _str_(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_by_category', args=[self.slug])

class Post(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = RichTextUploadingField(blank=True, null=True)
    title_tag = models.CharField(max_length=200, blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    #likes = models.ManyToManyField(User)
    post_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    title_description = RichTextUploadingField(blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.email

class SocialMedia(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    instagram_url = models.CharField(max_length=200, blank=True, null=True)
    whatsapp_url = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
class FileCourse(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    year = models.CharField(max_length=200,db_index=True)

    
    slug=models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('file_by_category', args=[self.slug])

class UploadFiles(models.Model):
    filecourse = models.ForeignKey(FileCourse, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    owner = models.CharField(max_length=200, blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Messages(models.Model):
    value = models.CharField(max_length=10000000, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=1000000)

class Message(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)

class chatMessages(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message