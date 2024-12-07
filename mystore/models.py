from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

    
class Store(models.Model):
    STORE_KINDS = [
        ('supermarket', 'Supermarket'),
        ('cafe', 'Cafe'),
        ('stationary', 'Stationary Store'),
        ('home_decor', 'Home Decor Store'),
        # Add more types as needed
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)  # City field for the store
    latitude = models.FloatField(default=0.0, blank=True)
    longitude = models.FloatField(default=0.0, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/store/profile_pictures/', blank=True, null=True)
    billboard_picture = models.ImageField(upload_to='uploads/store/billboard_pictures/', blank=True, null=True)
    store_kind = models.CharField(max_length=50, choices=STORE_KINDS, default='store', blank=False, null=False)

    def __str__(self): 
        return self.store_name


class Profile(models.Model):
    
    # Role Choices for Users (either 'store' or 'customer')
    ROLE_CHOICES = (
        ('store', 'Store'),
        ('customer', 'Customer'),
    )
    
    # Connect Profile to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Add role field with choices
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', blank=False)

    # Other fields
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # New field for approval status

    def __str__(self):
        return self.user.username

    
 
# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing
# post_save.connect(create_profile, sender=User)
    

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default='', blank=True)
    email = models.EmailField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)  # City field


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True)

    # Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def get_absolute_url(self):
            return reverse('product', args=[str(self.pk)])


# Customer Orders
class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    delivery_system = models.CharField(max_length=50, blank=True)  # Will hold "Delivery System 1" or "Delivery System 2"
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.product}'