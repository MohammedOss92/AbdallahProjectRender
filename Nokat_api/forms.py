from django import forms
from .models import *
from django.forms.widgets import ClearableFileInput
from django import forms



class ImgsFormss(forms.ModelForm):

    class Meta:
        model = ImagesNokat
        fields = [ 'new_img','pic', 'image_url', 'img_show']
        
        #pic = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        pic = forms.ImageField(required=True)
