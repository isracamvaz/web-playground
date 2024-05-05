from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Funcion para borrar la antigua imagen de avatar
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = custom_upload_to, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['user__username']


#Señal para cuando se cree un usuario, se cree el perfil
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print('Se acaba de crear un usuario y su perfil enlazado')