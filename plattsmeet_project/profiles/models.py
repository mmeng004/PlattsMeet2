from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.
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
    #settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    major = models.CharField(max_length=50, choices=MAJOR)
    pronouns = models.CharField(max_length=6, choices=PRONOUNS)
    hobbies = models.CharField(max_length=120)
    bio = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True )
    #friends = models.ManyToManyField("Profile", blank=True)

    def get_major(self):
        return self.major
    def get_pronouns(self):
        return self.pronouns
    def get_hobbies(self):
        return self.hobbies
    def get_bio(self):
        return self.bio
    def get_photo(self):
        return self.photo

