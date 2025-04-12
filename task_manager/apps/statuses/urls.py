from django.urls import path
from .views import (
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView
)
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', StatusListView.as_view(), name='statuses'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]
