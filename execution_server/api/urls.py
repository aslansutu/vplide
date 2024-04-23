from django.urls import re_path
from . import views

urlpatterns = [
    re_path("evaluate/", views.Evaluate.as_view(), name="evaluate"),
    re_path(
        "evaluate_scripts/", views.EvaluateScripts.as_view(), name="evaluate_scripts"
    ),
]
