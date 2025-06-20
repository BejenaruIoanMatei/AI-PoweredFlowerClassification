from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = models.TextField()
    # friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)

            if img.mode != "RGB":
                img = img.convert("RGB")

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                img.save(self.image.path)

        except UnidentifiedImageError:
            print(f"Could not identify image at {self.image.path}")
            
    # def get_friends(self):
    #     return self.friends.all()
    
    # def get_friends_no(self):
    #     return self.friends.all().count()    
    