from django.urls import path
from .views import LandingPage, StatementsDetailView, StatementsListView, UploadFileView

urlpatterns = [
    path("", LandingPage.as_view(), name="landing-page"),
    path("statements", StatementsListView.as_view(), name="statements-list"),
    path(
        "transactions/<uuid:unique_id>",
        StatementsDetailView.as_view(),
        name="transactions-list",
    ),
    path("upload", UploadFileView.as_view(), name="upload-statements"),
]
