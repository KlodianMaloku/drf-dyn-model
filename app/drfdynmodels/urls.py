from django.urls import path
from drfdynmodels.views import TableAPIView, UpdateTableAPIView, TableRowAPIView, TableRowsAPIView


urlpatterns = [
    path('table', TableAPIView.as_view(), name='create_table'),
    path('table/<str:id>', UpdateTableAPIView.as_view(), name='update_table'),
    path('table/<str:id>/row', TableRowAPIView.as_view(), name='add_row'),
    path('table/<str:id>/rows', TableRowsAPIView.as_view(), name='get_rows'),
]