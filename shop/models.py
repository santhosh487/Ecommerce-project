from django.db import models
from django.contrib.auth.models import User
import datetime
import os

# Function to rename uploaded files with timestamp
def getFileName(instance, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('upload/', new_filename)

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False, help_text='0-show, 1-Hidden')
    created_at = models.DateTimeField(auto_now_add=True)  # <-- FIXED LINE

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=150)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False, help_text='0-show, 1-Hidden')
    trending = models.BooleanField(default=False, help_text='0-default, 1-Trending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product.selling_price * self.product_qty
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

