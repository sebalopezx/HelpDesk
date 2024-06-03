from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from .models import *

@receiver(post_migrate)
def create_default_criticidades(sender, **kwargs):
    # Crear instancias de Priority si no existen
    Priority.objects.get_or_create(id=1, priority='Alta')
    Priority.objects.get_or_create(id=2, priority='Media')
    Priority.objects.get_or_create(id=3, priority='Baja')
    # Priority.objects.get_or_create(priority='Nula')


@receiver(post_migrate)
def create_default_tipo(sender, **kwargs):
    # Crear instancias de Tipo si no existen
    Type.objects.get_or_create(id=1, type='Felicitación')
    Type.objects.get_or_create(id=2, type='Consulta')
    Type.objects.get_or_create(id=3, type='Reclamo')


@receiver(post_migrate)
def create_default_estado(sender, **kwargs):
    # Crear instancias de Estado si no existen
    Status.objects.get_or_create(id=1, status='Nuevo')
    Status.objects.get_or_create(id=2, status='A resolución')
    Status.objects.get_or_create(id=3, status='Resuelto')
    Status.objects.get_or_create(id=4, status='No aplica')


@receiver(post_migrate)
def create_default_department(sender, **kwargs):
    Department.objects.get_or_create(id=1, department='Administración')
    Department.objects.get_or_create(id=2, department='Recepción')
    Department.objects.get_or_create(id=3, department='Atención')


@receiver(post_migrate)
def create_admin(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username='admin', 
        defaults={
            'email':'admin@gmail.com', 
            'is_superuser':True, 
            'is_staff':True, 
            'is_active':True, 
            'date_joined':timezone.now()
        })
    if created:
        user.set_password('123')
        user.save()
    
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'rut':'11.111.111-1',
            'phone':'123456789',
            'department_id':1
        }
    )


@receiver(post_migrate)
def create_agent(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username='recepcionista', 
        defaults={
            'first_name': 'Alan',
            'last_name': 'Brito',
            'email':'alan@gmail.com', 
            'is_superuser':False, 
            'is_staff':True, 
            'is_active':True, 
            'date_joined':timezone.now()
        })
    if created:
        user.set_password('123')
        user.save()
    
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'rut':'22.222.222-2',
            'phone':'11111111',
            'department_id':2
        }
    )

@receiver(post_migrate)
def create_agent(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username='atencion', 
        defaults={
            'first_name': 'Mario',
            'last_name': 'Neta',
            'email':'mario@gmail.com', 
            'is_superuser':False, 
            'is_staff':True, 
            'is_active':True, 
            'date_joined':timezone.now()
        })
    if created:
        user.set_password('123')
        user.save()
    
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'rut':'33.333.333-3',
            'phone':'222222222',
            'department_id':3
        }
    )

@receiver(post_migrate)
def create_user(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username='elsa', 
        defaults={
            'first_name': 'Elsa',
            'last_name': 'Broso',
            'email':'elsa@gmail.com', 
            'is_superuser':False, 
            'is_staff':False, 
            'is_active':True, 
            'date_joined':timezone.now()
        })
    if created:
        user.set_password('123')
        user.save()
    
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'rut':'44.444.444-4',
            'phone':'333333333',
            'department_id':''
        }
    )