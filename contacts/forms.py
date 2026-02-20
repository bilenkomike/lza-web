from django import forms
from .models import NewsletterSubscriber
from .utils import t

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]



