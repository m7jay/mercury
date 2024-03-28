from django.urls import path
from .views import (
    StatementsDetailView,
    StatementsListView,
    UploadFileView,
    TagsSummaryView,
)

urlpatterns = [
    path("", StatementsListView.as_view(), name="statements-list"),
    path(
        "transactions/<uuid:unique_id>",
        StatementsDetailView.as_view(),
        name="transactions-list",
    ),
    path(
        "transactions/<uuid:unique_id>/tags",
        TagsSummaryView.as_view(),
        name="transactions-tags",
    ),
    path("upload", UploadFileView.as_view(), name="upload-statements"),
]
