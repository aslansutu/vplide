from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        "init/", views.InitializeRepository.as_view(), name="initialize_repository"
    ),
    re_path("commit/", views.CommitChanges.as_view(), name="commit_changes"),
    re_path("fetch/", views.GetSourceCode.as_view(), name="evaluate"),
]
