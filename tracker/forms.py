from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobApplication


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "company_name", "job_title", "job_location", "job_link",
            "status", "date_applied", "interview_date", "notes",
            "cv", "cover_letter",
        ]
        widgets = {
            "date_applied":    forms.DateInput(attrs={"type": "date"}),
            "interview_date":  forms.DateInput(attrs={"type": "date"}),
            "notes":           forms.Textarea(attrs={"rows": 4}),
        }


class QuickStatusForm(forms.ModelForm):
    """Minimal form used for inline status updates in the list view."""
    class Meta:
        model = JobApplication
        fields = ["status"]
