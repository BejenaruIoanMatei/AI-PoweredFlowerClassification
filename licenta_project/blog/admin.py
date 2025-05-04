from django.contrib import admin
from .models import Post, ImageClassification, Activity

admin.site.register(Post)
admin.site.register(ImageClassification)
admin.site.register(Activity)