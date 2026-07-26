from django import forms

from .models import UserProfile


class RecommenderForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
    )
    user_type = forms.ChoiceField(
        choices=UserProfile.UserType.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    goal = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "e.g. I want to learn Python.",
            }
        )
    )


class PromptGeneratorForm(forms.Form):
    task = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Write a tourism blog."}),
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 5, "placeholder": "How can we help?"}
        )
    )
