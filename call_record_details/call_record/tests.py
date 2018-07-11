from django.test import TestCase

from .models import Record_model
from datetime import datetime

class RecordTestCase(TestCase):

    def setUp(self):

        Record_model.objects.create(
            type=0,
            call_id=70,
            time="2017-12-12T15:07:13Z",
            origin_phone_number="99988526423",
            destination_phone_number="9993468278"
        )


    def test_record_model(self):
        start = Record_model.objects.get(call_id=70,type=0)
        date = datetime.strptime("2017-12-12T15:07:13Z", "%Y-%m-%dT%H:%M:%SZ")

        self.assertEqual(start.time.strftime("%Y-%m-%d %H:%M:%S"),date.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(start.call_id, 70)
        self.assertEqual(start.origin_phone_number,"99988526423")
        self.assertEqual(start.destination_phone_number,"9993468278")