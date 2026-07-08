from django.conf import settings
from django.db import models
from django.urls import reverse


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Interview", "Interview"),
        ("Rejected", "Rejected"),
        ("Offer", "Offer"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company_name  = models.CharField(max_length=150)
    job_title     = models.CharField(max_length=150)
    job_location  = models.CharField(max_length=150, blank=True)
    job_link      = models.URLField(blank=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Applied")
    date_applied  = models.DateField()
    # ✅ NEW: optional interview / follow-up date
    interview_date = models.DateField(null=True, blank=True, help_text="Date of interview or next follow-up")
    notes         = models.TextField(blank=True)
    cv            = models.FileField(upload_to="cvs/", blank=True, null=True)
    cover_letter  = models.FileField(upload_to="cover_letters/", blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_applied", "-created_at"]

    def __str__(self):
        return f"{self.job_title} @ {self.company_name} ({self.status})"

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})
