from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from datetime import date



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email adresi gereklidir.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Sosyal', 'Sosyal'),
        ('Konferans', 'Konferans'),
        ('Workshop', 'Workshop'),
        ('Online', 'Online'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='Genel')
    sub_category = models.CharField(max_length=255, null=True, blank=True) 
    duration = models.DurationField()
    photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='owned_events', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_events',
        blank=True  
    )
    def is_upcoming(self):
        today = date.today()
        return 1 if self.event_date >= today else 0

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    score = models.IntegerField(default=0)
    first_participation = models.BooleanField(default=False)
    participated_events_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_profile.png')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Yorum: {self.content[:20]}... - {self.user.username}"