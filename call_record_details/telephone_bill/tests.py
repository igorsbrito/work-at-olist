from django.test import TestCase

from .views import TelephoneCallBillViewSet
from .models import Telephone_bill_call_model
from call_record.models import Record_model

from datetime import datetime



class TelephoneBillTestCase(TestCase):

    def setUp(self):
        Record_model.objects.create(
            type=0,
            call_id=70,
            timestamp="2016-02-29T21:57:13Z",
            source="99988526423",
            destination="9993468278"
        )

        Record_model.objects.create(
            type=1,
            call_id=70,
            timestamp="2016-02-29T22:10:56Z",
        )

    def test_paid_minutes(self):
        call_start1 = datetime.strptime("2016-02-29T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end1   = datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

        call_start2 = datetime.strptime("2016-02-29T04:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end2 = datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

        call_start3 = datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end3 = datetime.strptime("2017-12-13T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ")

        telephoneCallBillViewSet = TelephoneCallBillViewSet()

        data1 = telephoneCallBillViewSet.get_paid_minutes(call_start1, call_end1)
        data2 = telephoneCallBillViewSet.get_paid_minutes(call_start2, call_end2)
        data3 = telephoneCallBillViewSet.get_paid_minutes(call_start3, call_end3)

        self.assertEqual(data1['minutes_standard'], 120)
        self.assertEqual(data2['minutes_standard'], 480)
        self.assertEqual(data3['minutes_standard'], 962)


    def test_create_telephone_bill(self):

        telephoneCallBillViewSet = TelephoneCallBillViewSet()

        telephoneCallBillViewSet.create_telephone_bill(70)

        telephoneBill = Telephone_bill_call_model.objects.filter(call_id=70)

        self.assertEqual(float(telephoneBill[0].call_price), 0.54)


