from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import user_profile
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='normaluser')
        instance.groups.add(group)

        # Delete existing Employee_profile objects for the user
        user_profile.objects.filter(user=instance).delete()

        # Create new Employee_profile object
        user_profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

post_save.connect(customer_profile, sender=User)

