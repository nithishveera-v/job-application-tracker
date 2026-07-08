from django.urls import path
from . import views

urlpatterns = [
    path("",                                   views.dashboard,             name="dashboard"),
    path("signup/",                            views.SignUpView.as_view(),   name="signup"),
    path("login/",                             views.CustomLoginView.as_view(), name="login"),
    path("logout/",                            views.CustomLogoutView.as_view(), name="logout"),
    path("applications/",                      views.application_list,      name="application_list"),
    path("applications/add/",                  views.application_create,    name="application_create"),
    path("applications/<int:pk>/",             views.application_detail,    name="application_detail"),
    path("applications/<int:pk>/edit/",        views.application_update,    name="application_update"),
    path("applications/<int:pk>/delete/",      views.application_delete,    name="application_delete"),
    # ✅ New routes
    path("applications/<int:pk>/status/",      views.quick_status_update,   name="quick_status_update"),
    path("applications/export/csv/",           views.export_csv,            name="export_csv"),
]
