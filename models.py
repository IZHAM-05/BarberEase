from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    USER_TYPES = (
        ("Admin", "Admin"),
        ("Owner", "Owner"),
        ("Customer", "Customer"),
    )
    usertype = models.CharField(max_length=20, choices=USER_TYPES, default="Customer")

    def __str__(self):
        return f"{self.username} ({self.usertype})"


class Barbershop(models.Model):
    # FK to the auth user who owns the shop
    usrname = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    # optional plain-text password for admin view (academic/demo only — DO NOT use in production)
    password_raw = models.CharField(max_length=128, blank=True, null=True)

    name = models.CharField(max_length=50)                # owner full name or contact name
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    shop_name = models.CharField(max_length=100)
    shop_address = models.CharField(max_length=200, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)     # admin should approve owner/shop
    created_at = models.DateTimeField(auto_now_add=True)
    license_image = models.ImageField(upload_to="shop_licenses/", blank=True, null=True)

    def __str__(self):
        return self.shop_name
    
class ShopImage(models.Model):
    shop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="shops/")

    def __str__(self):
        return f"Image for {self.shop.shop_name}"



class Customer(models.Model):
    usrname = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    # optional plain-text password for admin view (academic/demo only — DO NOT use in production)
    password_raw = models.CharField(max_length=128, blank=True, null=True)

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(blank=True)
    profile_pic = models.ImageField(upload_to='customers/', null=True, blank=True)  # NEW FIELD

    def __str__(self):
        return self.name


class Service(models.Model):
    shop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.IntegerField(default=30, help_text="Duration in minutes")
    image = models.ImageField(upload_to='services/', null=True, blank=True)  # NEW


    def __str__(self):
        return f"{self.service_name} - {self.shop.shop_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        (0, "Pending"),
        (1, "Approved"),    
        (2, "Rejected"),
        (3, "Completed")   # <--- Add this

    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    shop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} → {self.shop.shop_name} ({self.get_status_display()})"


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    shop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} review for {self.shop.shop_name}"
