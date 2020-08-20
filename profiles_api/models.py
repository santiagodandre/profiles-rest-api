from django.db import models
# Clases que necesito para override django user model 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Get info from settings.py's project file to get AUTH_USER_MODEL
from django.conf import settings

# Create your models here.

class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    
    def create_user(self, email, name, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        #Normalizar email 
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        # Para asegurar que el password sea encriptado
        user.set_password(password)
        # Save the user model / Especificar la db es buena practica, no requerido
        user.save(using=self._db)     
        return user 

    def create_superuser(self, email, name, password):
        """ Create and save a new superuser  """
        user = self.create_user(email, name, password)
        # From PermissionsMixin
        user.is_superuser = True 
        user.is_staff = True
        user.save(using=self._db)
        return user 
          


class UserProfile(AbstractBaseUser, PermissionsMixin): 
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    full_mame = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # is_staff para determinar si es un usuario admin 
    is_staff = models.BooleanField(default=False)

    #Comment

    # Specify the model manager . Required to use our custom User model. Needs a custom manager for the user model
    objects = UserProfileManager()
    
    # override default username field. so we identify users with email  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """ Retrieve short name of user """
        return self.name

    # Specify the string representation of the model, with special method __str__
    # Es recomendable siempre hacerlo 
    def __str__(self):
        """ Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """ Profile status update """ 

    user_profile = models.ForeignKey(
        # Se podría usar directamente el nombre de la clase, pero es buen práctica levantar la clase User configurada en settings.py 
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    # String representation of the model 
    def __str__(self):
        """ Return the model as a string """
        return self.status_text