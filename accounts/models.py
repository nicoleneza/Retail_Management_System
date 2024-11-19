from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    points = models.IntegerField(default=0)
    address = models.TextField(blank=True)
    
    # Override the groups field with a custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',  # Custom related_name
        help_text='The groups this user belongs to.'
    )

    # Override the user_permissions field with a custom related_name
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',  # Custom related_name
        help_text='Specific permissions for this user.'
    )
    
    def __str__(self):
        return self.username 

class UserProfile(models.Model):
    USER_TYPES = (
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    points = models.IntegerField(default=0)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.user_type})"
    
    def add_points(self, amount):
        """Add points based on purchase amount"""
        new_points = int(amount * 10)  # $1 = 10 points
        self.points += new_points
        self.save()
        return new_points

# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()