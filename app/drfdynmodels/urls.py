
from django.urls import path, include
from drfdynmodels.views import TableAPIView, TableActionsView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', TableActionsView, basename='table-actions')

urlpatterns = [
    path('table', TableAPIView.as_view(), name='create-table'),
    path('table/<str:id>/', include(router.urls))
]