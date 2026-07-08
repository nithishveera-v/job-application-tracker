import csv
from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .forms import JobApplicationForm, QuickStatusForm, SignUpForm
from .models import JobApplication


# ─── Auth ────────────────────────────────────────────────────────────────────

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Account created. You can now log in.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):
    next_page = "login"


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    qs = JobApplication.objects.filter(user=request.user)
    total = qs.count()

    status_summary = {c[0]: 0 for c in JobApplication.STATUS_CHOICES}
    for row in qs.values("status").annotate(n=Count("status")):
        status_summary[row["status"]] = row["n"]

    # Upcoming interviews (today or later, sorted soonest first)
    upcoming = (
        qs.filter(interview_date__gte=date.today())
        .exclude(status="Rejected")
        .order_by("interview_date")[:5]
    )

    recent = qs[:5]

    return render(request, "tracker/dashboard.html", {
        "total": total,
        "status_summary": status_summary,
        "recent_applications": recent,
        "upcoming_interviews": upcoming,
    })


# ─── Application list (with pagination + search/filter) ──────────────────────

@login_required
def application_list(request):
    qs = JobApplication.objects.filter(user=request.user)

    status_filter = request.GET.get("status", "")
    search_query  = request.GET.get("q", "")

    if status_filter:
        qs = qs.filter(status=status_filter)
    if search_query:
        qs = qs.filter(
            Q(company_name__icontains=search_query) |
            Q(job_title__icontains=search_query)
        )

    # ✅ Pagination — 10 per page
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tracker/application_list.html", {
        "page_obj": page_obj,
        "status_choices": JobApplication.STATUS_CHOICES,
        "status_filter": status_filter,
        "search_query": search_query,
    })


# ─── CRUD ─────────────────────────────────────────────────────────────────────

@login_required
def application_detail(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    return render(request, "tracker/application_detail.html", {"application": app})


@login_required
def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Application added.")
            return redirect("application_list")
    else:
        form = JobApplicationForm()
    return render(request, "tracker/application_form.html", {"form": form, "title": "Add Application"})


@login_required
def application_update(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated.")
            return redirect("application_detail", pk=app.pk)
    else:
        form = JobApplicationForm(instance=app)
    return render(request, "tracker/application_form.html", {"form": form, "title": "Edit Application"})


@login_required
def application_delete(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        app.delete()
        messages.success(request, "Application deleted.")
        return redirect("application_list")
    return render(request, "tracker/application_confirm_delete.html", {"application": app})


# ─── ✅ Quick inline status update (AJAX-friendly) ────────────────────────────

@login_required
@require_POST
def quick_status_update(request, pk):
    app = get_object_or_404(JobApplication, pk=pk, user=request.user)
    form = QuickStatusForm(request.POST, instance=app)
    if form.is_valid():
        form.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": app.status})
        messages.success(request, f"Status updated to {app.status}.")
    return redirect("application_list")


# ─── ✅ CSV Export ─────────────────────────────────────────────────────────────

@login_required
def export_csv(request):
    qs = JobApplication.objects.filter(user=request.user)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="job_applications.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Company", "Job Title", "Location", "Status",
        "Date Applied", "Interview Date", "Job Link", "Notes",
    ])
    for app in qs:
        writer.writerow([
            app.company_name, app.job_title, app.job_location, app.status,
            app.date_applied, app.interview_date or "", app.job_link, app.notes,
        ])
    return response
