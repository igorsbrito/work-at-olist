from django.test import TestCase

from .models import Record_model
from datetime import datetime

class RecordTestCase(TestCase):

    def setUp(self):

        Record_model.objects.create(
            type=0,
            call_id=70,
            timestamp="2017-12-12T15:07:13Z",
            source="99988526423",
            destination="9993468278"
        )


    def test_record_model(self):
        start = Record_model.objects.get(call_id=70,type=0)
        date = datetime.strptime("2017-12-12T15:07:13Z", "%Y-%m-%dT%H:%M:%SZ")

        self.assertEqual(start.timestamp.strftime("%Y-%m-%d %H:%M:%S"),date.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(start.call_id, 70)
        self.assertEqual(start.source,"99988526423")
        self.assertEqual(start.destination,"9993468278")

    def teste_call_record_create(self):
        data ={
            'call_id':70,
            'type':1,
            'timestamp':'2016-02-29T14:00:00Z',
        }

        response = self.client.post('/record/record_call/', data,follow=True)
        self.assertEqual(response.status_code,201)

        #This second insertion should not create a new call_record because already exist in the database one call_record with this call id and this type.
        response = self.client.post('/record/record_call/', data, follow=True)
        self.assertEqual(response.status_code, 400)
