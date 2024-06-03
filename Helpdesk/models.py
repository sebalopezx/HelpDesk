import email
from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.


class Priority(models.Model):
    priority = models.CharField(
        max_length=45,
        blank=True,
        null=True, 
        verbose_name="Prioridad",
        )

    def __str__(self):
        return self.priority


class Status(models.Model):
    status = models.CharField(
        max_length=45,
        verbose_name="Estado",
        default="Abierto"
        )  # permite el cambio de estado de tique de los ejecutivos

    def __str__(self):
        return self.status


class Type(models.Model):
    type = models.CharField(
        max_length=45, 
        verbose_name="Tipo"
        )

    def __str__(self):
        return self.type


class Department(models.Model):
    department = models.CharField(
        max_length=100, 
        verbose_name="Área"
        )

    def __str__(self):
        return self.department


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    phone = models.CharField(max_length=9, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.rut}" # {self.user.get_full_name()} ({self.user.username} - 


class Ticket(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    opening_agent = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, related_name='opening_agent')
    closure_agent = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE, related_name='closure_agent')
    issue = models.CharField(max_length=200)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    observation = models.TextField(max_length=255)
    solution = models.TextField(max_length=255, blank=True)
    opening_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.issue}"






