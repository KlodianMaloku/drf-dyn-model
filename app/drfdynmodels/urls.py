from django.urls import include, path
from rest_framework import routers
from drfdynmodels.views import JustAModelViewset

router = routers.DefaultRouter()
router.register(r'', JustAModelViewset, basename='justamodel')


urlpatterns = [
    path('', include(router.urls)),
]

