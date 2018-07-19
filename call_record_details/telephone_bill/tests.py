from django.test import TestCase

from .views import TelephoneCallBillViewSet
from .models import Telephone_bill_call_model
from call_record.models import Record_model

from datetime import datetime



class TelephoneBillTestCase(TestCase):

    def setUp(self):
        call_start_date = datetime.strptime("2016-02-29T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end_date = datetime.strptime("2016-02-29T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ")

        Record_model.objects.create(
            type=0,
            call_id=70,
            timestamp=call_start_date,
            source="99988526423",
            destination="9993468278"
        )

        Record_model.objects.create(
            type=1,
            call_id=70,
            timestamp=call_end_date,
        )

    def test_paid_minutes(self):
        call_start1 = datetime.strptime("2016-02-29T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end1   = datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

        call_start2 = datetime.strptime("2016-02-29T04:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end2 = datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

        call_start3 = datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end3 = datetime.strptime("2017-12-13T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ")

        call_start4 = datetime.strptime("2017-12-12T15:07:58Z","%Y-%m-%dT%H:%M:%SZ")
        call_end4 = datetime.strptime("2017-12-12T15:12:56Z", "%Y-%m-%dT%H:%M:%SZ" )

        telephoneCallBillViewSet = TelephoneCallBillViewSet()

        data1 = telephoneCallBillViewSet.get_paid_minutes(call_start1, call_end1)
        data2 = telephoneCallBillViewSet.get_paid_minutes(call_start2, call_end2)
        data3 = telephoneCallBillViewSet.get_paid_minutes(call_start3, call_end3)
        date4 = telephoneCallBillViewSet.get_paid_minutes(call_start4, call_end4)

        self.assertEqual(data1['minutes_standard'], 120)
        self.assertEqual(data2['minutes_standard'], 480)
        self.assertEqual(data3['minutes_standard'], 962)
        self.assertEqual(date4['minutes_standard'], 4)


    def test_build_call_price(self):
        call_start = datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ")
        call_end = datetime.strptime("2017-12-13T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ")

        telephoneCallBillViewSet = TelephoneCallBillViewSet()

        price = telephoneCallBillViewSet.build_call_price(call_start, call_end)

        self.assertEqual(price, 86.94)



    def test_create_telephone_bill(self):

        telephoneCallBillViewSet = TelephoneCallBillViewSet()

        telephoneCallBillViewSet.create_telephone_bill(70)

        telephoneBill = Telephone_bill_call_model.objects.filter(call_id=70)

        self.assertEqual(float(telephoneBill[0].call_price), 0.54)

