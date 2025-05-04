from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image, UnidentifiedImageError
from virtual_garden.models import Flower


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_post = models.ImageField(upload_to='post_images')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image_post.path)
            
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if img.height > 400 or img.width > 400:
                output_size = (400,400)
                img.thumbnail(output_size)
                img.save(self.image_post.path)
                
        except UnidentifiedImageError:
            print(f"Could not identify image at {self.image_post.path}")

class ImageClassification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='classified_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    predicted_label = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if img.height > 400 or img.width > 400:
                output_size = (400,400)
                img.thumbnail(output_size)
                img.save(self.image.path)
                
        except UnidentifiedImageError:
            print(f"Could not identify image at {self.image.path}")

    def __str__(self):
        return f"{self.user.username} - {self.predicted_label or 'Unclassified'}"
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.message or f"{self.user.username} did something idunno"