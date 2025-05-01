from django import forms
from .models import ImageClassification

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageClassification
        fields = ['image']
