from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# comment by farouk "i did not use the django forms I used regular html forms and passed the data threw the post request"
# this page is useless for now

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        





# class ContactForm(forms.Form):
#     name = forms.CharField(
#         widget=forms.TextInput(attrs={"class": "contact-us-form-text"}), max_length=100
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={"class": "contact-us-form-text"}), required=True
#     )
#     subject = forms.CharField(
#         widget=forms.TextInput(attrs={"class": "contact-us-form-text"}), max_length=100
#     )
#     message = forms.CharField(
#         widget=forms.TextInput(attrs={"class": "contact-us-form-text"})
#     )

#     def __init__(self):
#         super().__init__()

#         self.helper = FormHelper

#         self.helper.form_method = "post"

#         self.helper.layout = Layout(
#             "name", "email", "subject", "message", Submit("submit", "Submit")
#         )


# class MapForm(forms.Form):
#     coords = forms.CharField(
#         label="Choose coordinates from map",
#         widget=forms.TextInput(
#             attrs={
#                 "class": "contact-us-form-text",
#                 "placeholder": "Coordinates",
#                 "readonly": "readonly",
#                 "id": "coords",
#             }
#         ),
#     )

#     crop_selections = [
#         ("banana", "Banana"),
#         ("soyabean", "Soyabean"),
#         ("cabbage", "Cabbage"),
#         ("potato", "Potato"),
#         ("rice", "Rice"),
#         ("melon", "Melon"),
#         ("maize", "Maize"),
#         ("citrus", "Citrus"),
#         ("bean", "Bean"),
#         ("wheat", "Wheat"),
#         ("mustard", "Mustard"),
#         ("cotton", "Cotton"),
#         ("sugarcane", "Sugarcane"),
#         ("tomato", "Tomato"),
#         ("onion", "Onion"),
#     ]
#     crop = forms.CharField(
#         label="Choose Crop",
#         widget=forms.Select(
#             choices=crop_selections,
#             attrs={"class": "contact-us-form-text"},
#         ),
#     )

#     def __init__(self):
#         super().__init__()

#         self.helper = FormHelper

#         self.helper.form_method = "post"

#         self.helper.layout = Layout(
#             "coords",
#             "crop",
#             Submit("submit", "Submit", css_class="contact-us-form-btn"),
#         )

