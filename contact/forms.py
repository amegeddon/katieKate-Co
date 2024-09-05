from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email Address')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')
    photo = forms.ImageField(required=False)
