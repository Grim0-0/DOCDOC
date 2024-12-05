from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='documents/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class image_classification(models.Model):
    pic=models.ImageField(upload_to='images')