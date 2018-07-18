from django.conf.urls import include, url
from rest_framework import routers

from .views import TelephoneCallBillViewSet

router = routers.DefaultRouter()
router.register(r'telephone_call_bill', TelephoneCallBillViewSet)

urlpatterns =[
    url(r'', include(router.urls)),
]
