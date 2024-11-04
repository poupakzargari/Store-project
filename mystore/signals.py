from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Store, Customer
from django.contrib.auth.models import User
from .forms import SignUpForm

# @receiver(post_save, sender=Profile)
# def create_store_instance(sender, instance, created, **kwargs):
#     # Automatically create a Store instance if the user's role is 'store'
#     if created and instance.role == 'store':
#         # Create a Store instance linked to this profile's user
#         Store.objects.get_or_create(user=instance.user)


# @receiver(post_save, sender=Profile)
# def create_customer_instance(sender, instance, created, **kwargs):
#     if created and instance.role == 'customer':
#         Customer.objects.get_or_create(user=instance.user)
