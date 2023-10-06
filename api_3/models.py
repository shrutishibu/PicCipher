from django.db import models

class GroceryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class GroceryReceipt(models.Model):
    date = models.DateField()
    items = models.ManyToManyField(GroceryItem)

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    
from djongo import models

class ImageData(models.Model):
    image_url = models.URLField()
    ocr_text = models.TextField()
    tags = models.FileField(
        max_length=1000,  # Set the maximum length for items in the list
        null=True,      # Allow the field to be null (if desired)
    )