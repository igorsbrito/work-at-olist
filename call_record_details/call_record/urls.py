from django.conf.urls import include, url
from rest_framework import routers

from .views import RecordViewSet

router = routers.DefaultRouter()
router.register(r'record_call', RecordViewSet)

urlpatterns =[
    url(r'', include(router.urls)),
]
