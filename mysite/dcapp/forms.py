from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Document, image_classification

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['image',]

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image to classify')

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ClassifyForm(forms.Form):
    file = forms.ImageField()

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 10 * 1024 * 1024:  # limit to 10MB
                raise forms.ValidationError("File size too large ( > 10mb )")
            return file
        else:
            raise forms.ValidationError("Couldn't read uploaded file")