from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save

#username - proper ones rather than ID values
from autoslug import AutoSlugField

#custom account model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Email address Required!')
		if not username:
			raise ValueError('Username Required!')
		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "codingwithmitch/default_profile_image.png"

#custom account model
class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

#Models for Profiles
#required for a friend request
class Profile(models.Model):
    MAJOR = (
        ('Accounting','Accounting'),
        ('Africana Studies','Africana Studies'),
        ('Anthropology','Anthropology'),
        ('Art','Art'),
        ('Art Studio','Art Studio'),
        ('Audio-Radio Production','Audio-Radio Production'),
        ('Biochemistry','Biochemistry'),
        ('Biology','Biology'),
        ('Biomedical Sciences','Biomedical Sciences'),
        ('Broadcast Journalism','Broadcast Journalism'),
        ('Business Administration','Business Administration'),
        ('Chemistry','Chemistry'),
        ('Childhood Education','Childhood Education'),
        ('Communication Sciences and Disorders','Communication Sciences and Disorders'),
        ('Communication Studies','Communication Studies'),
        ('Computer Science','Computer Science'),
        ('Computer Security','Computer Security'),
        ('Criminal Justice','Criminal Justice'),
        ('Digital Media Production','Digital Media Production'),
        ('Earth Science','Earth Science'),
        ('Ecology','Ecology'),
        ('Economics','Economics'),
        ('English:Language Arts','English:Language Arts'),
        ('English:Literature','English:Literature'),
        ('English:Writing Arts','English:Writing Arts'),
        ('Entrepreneurship','Entrepreneurship'),
        ('Environmental Geosciences','Environmental Geosciences'),
        ('Environmental Science','Environmental Science'),
        ('Environmental Studies','Environmental Studies'),
        ('Expeditionary Studies','Expeditionary Studies'),
        ('Finance','Finance'),
        ('Fitness and Wellness Leadership','Fitness and Wellness Leadership'),
        ('Gender and Women Studies','Gender and Women Studies'),
        ('Geology','Geology'),
        ('Global Supply Chain Management','Global Supply Chain Management'),
        ('History','History'),
        ('Hospitality Management','Hospitality Management'),
        ('Human Development and Family Relations','Human Development and Family Relations'),
        ('Individualized Studies','Individualized Studies'),
        ('Information Technology','Information Technology'),
        ('International Business','International Business'),
        ('Journalism','Journalism'),
        ('Latin American Studies','Latin American Studies'),
        ('Law and Justice','Law and Justice'),
        ('Management','Management'),
        ('Management Information Systems','Management Information Systems'),
        ('Marketing','Marketing'),
        ('Mathematics','Mathematics'),
        ('Medical Technology','Medical Technology'),
        ('Music','Music'),
        ('Music Arts Management','Music Arts Management'),
        ('Nursing','Nursing'),
        ('Nutrition','Nutrition'),
        ('Philosophy','Philosophy'),
        ('Physics','Physics'),
        ('Political Science','Political Science'),
        ('Psychology','Psychology'),
        ('Public Relations','Public Relations'),
        ('Robotics','Robotics'),
        ('Social Work','Social Work'),
        ('Sociology','Sociology'),
        ('Spanish','Spanish'),
        ('Spanish Language Broadcasting','Spanish Language Broadcasting'),
        ('Theatre','Theatre'),
        ('TV-Video Production','TV-Video Production'),
    )
    PRONOUNS = (
        ('He','He/Him/His'),
        ('She','She/Her/Hers'),
        ('They','They/Them/Theirs'),
        ('Ze','Ze/Hir/Hirs'),
    )
    #first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    major = models.CharField(max_length=50, choices=MAJOR)
    pronouns = models.CharField(max_length=6, choices=PRONOUNS)
    hobbies = models.CharField(max_length=120)
    bio = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True )
    friends = models.ManyToManyField("Profile", blank=True)