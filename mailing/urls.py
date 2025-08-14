from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingCreateView, MailingDeleteView,
                           MailingListView, MailingUpdateView, sending_mailing, complete_mailing)

app_name = MailingConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing"),
    path("create_mailing/", MailingCreateView.as_view(), name="create_mailing"),
    path("update_mailing/<int:pk>/", MailingUpdateView.as_view(), name="update_mailing"),
    path("delete_mailing/<int:pk>/", MailingDeleteView.as_view(), name="delete_mailing"),
    path("sending_mailing/<int:pk>/", sending_mailing, name="sending_mailing"),
    path("complete_mailing/<int:pk>/", complete_mailing, name="complete_mailing")
]
