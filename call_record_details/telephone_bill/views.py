from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from call_record.views import Record_model
from .models import Telephone_bill_call_model
from .serializer import Telephone_bill_call_serializer

from math import floor
import datetime


class TelephoneCallBillViewSet(viewsets.ModelViewSet):
    queryset = Telephone_bill_call_model.objects.all()
    serializer_class = Telephone_bill_call_serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    START_STANDARD_HOUR = 6
    END_STANDARD_HOUR = 22

    def create_telephone_bill(self, call_id):

        data = self.build_call_bill_data(call_id)

        total_price = self.build_call_price(data['call_start'], data['call_end'])

        telephoneBill = Telephone_bill_call_model.objects.create(call_id=call_id,
                                                                 source=data['source'],
                                                                 destination=data['destination'],
                                                                 call_price=total_price,
                                                                 call_start=data['call_start'],
                                                                 call_end=data['call_end'],
                                                                 call_duration=data['call_duration'])

    def build_call_price(self, call_start, call_end):

        base_chrage = 0.36
        standard_charge_per_minute = 0.09
        reduce_charge_per_minute = 0.0

        minutes = self.get_paid_minutes(call_start, call_end)

        total_price_standard = round(standard_charge_per_minute * minutes['minutes_standard'], 2)
        total_price_reduce = round(reduce_charge_per_minute * minutes['minutes_reduce'], 2)

        total_price =  base_chrage + total_price_standard + total_price_reduce

        return total_price


    def build_call_bill_data(self, call_id):

        start_call = Record_model.objects.get(call_id=call_id, type=0)
        end_call = Record_model.objects.get(call_id=call_id, type=1)


        duration = end_call.timestamp - start_call.timestamp

        call_duration = datetime.time(duration.days *24+ duration.seconds//3600, (duration.seconds//60)%60)

        return  {
            'call_duration' : call_duration,
            'source' :start_call.source,
            'destination' :start_call.destination,
            'call_start' :start_call.timestamp,
            'call_end' :end_call.timestamp,

        }


    def standard_hour(self, hour):
        return (self.START_STANDARD_HOUR <= hour and self.END_STANDARD_HOUR > hour)

    def reduce_hour(self, hour):
        return (self.START_STANDARD_HOUR > hour or self.END_STANDARD_HOUR <= hour)


    def get_paid_minutes(self, call_start, call_end):
        start_hour = call_start.hour
        end_hour = call_end.hour

        total_duration = call_end - call_start
        total_hours = (total_duration.seconds/3600) + (total_duration.days*24)

        # if the call start and end in the same day
        if total_hours < 24:

            # the call start and end between 6 and 22
            if self.standard_hour(start_hour) and self.standard_hour(end_hour):
                duration_standard = total_duration
                duration_reduce = datetime.timedelta(hours=0, minutes=0)

            # the call start between 6 and 22 and end between 22 and 6
            elif self.standard_hour(start_hour) and self.reduce_hour(end_hour):
                #hour_to_end = self.END_STANDARD_HOUR - start_hour
                date_aux = datetime.datetime(call_start.year, call_start.month, call_start.day, 22, 00, tzinfo=call_start.tzinfo)

                duration_reduce = call_end - date_aux
                duration_standard = total_duration - duration_reduce

            # the call start between 22 and 6 and end between 6 and 22
            elif self.reduce_hour(start_hour) and self.standard_hour(end_hour):
                hour_to_end = end_hour - self.START_STANDARD_HOUR
                date_aux = datetime.datetime(call_end.year, call_end.month, call_end.day, 6, 00)

                duration_reduce = date_aux - call_start
                duration_standard = total_duration - duration_reduce


            elif self.reduce_hour(start_hour) and self.reduce_hour(end_hour):
                duration = self.END_STANDARD_HOUR - self.START_STANDARD_HOUR

                duration_aux = call_end- call_start
                if (duration_aux.seconds/ 3600) < 8:
                    duration_standard = datetime.timedelta(hours=0, minutes=0, seconds=0, milliseconds=0)
                    duration_reduce = call_end - call_start

                else:
                    date_aux_start = datetime.datetime(call_start.year, call_start.month, call_start.day, 6, 00)
                    date_aux_end = datetime.datetime(call_end.year, call_end.month, call_end.day, 22, 00)

                    duration_standard = datetime.timedelta(hours=16, minutes=0, seconds=0, milliseconds=0)
                    duration_reduce = (date_aux_start - call_start) + (call_end - date_aux_end)


        # if the call start in a day and end in another day
        else:

            duration_recude_hours_default = datetime.timedelta(hours=8, minutes=0, seconds=0, milliseconds=0)

            # the call start and end between 6 and 22
            if self.standard_hour(start_hour) and self.standard_hour(end_hour):

                days = floor(total_hours / 24)

                duration_standard = total_duration - days*duration_recude_hours_default
                duration_reduce = days*duration_recude_hours_default

            # the call start between 6 and 22 and end between 22 and 6
            elif self.standard_hour(start_hour) and self.reduce_hour(end_hour):

                days = floor(total_hours / 24)

                # 22 hour of the day that the call ended

                if end_hour < 6:
                    date_aux = datetime.datetime(call_end.year, call_end.month, call_end.day, 22, 00)- datetime.timedelta(days=1)
                else:
                    date_aux = datetime.datetime(call_end.year, call_end.month, call_end.day, 22, 00)


                # this is the duration between 22 hour and the time that the call end
                duration_recude_hours = call_end - date_aux

                duration_reduce = (days*duration_recude_hours_default) + duration_recude_hours
                duration_standard = total_duration - duration_reduce

            elif self.reduce_hour(start_hour) and self.standard_hour(end_hour):

                days = floor(total_hours / 24)

                # 22 hour of the day that the call ended
                if start_hour < 6:
                    date_aux = datetime.datetime(call_start.year, call_start.month, call_start.day, 6, 00)
                else:
                    date_aux = datetime.datetime(call_start.year, call_start.month, call_start.day, 6, 00) + datetime.timedelta(days=1)

                # this is the duration between  the hour the call start and 6
                duration_recude_hours = date_aux  - call_start

                duration_reduce = (days * duration_recude_hours_default) + duration_recude_hours
                duration_standard = total_duration - duration_reduce

            elif self.reduce_hour(start_hour) and self.reduce_hour(end_hour):

                days = floor(total_hours / 24)

                if start_hour < 6:
                    date_aux_start = datetime.datetime(call_start.year, call_start.month, call_start.day, 6, 00)
                else:
                    date_aux_start = datetime.datetime(call_start.year, call_start.month, call_start.day, 6, 00) + datetime.timedelta(days=1)

                if end_hour < 6:
                    date_aux_end = datetime.datetime(call_end.year, call_end.month, call_end.day, 22, 00) - datetime.timedelta(days=1)
                else:
                    date_aux_end = datetime.datetime(call_end.year, call_end.month, call_end.day, 22, 00)

                duration_recude_hours_start = date_aux_start - call_start
                duration_reduce_hours_end = call_end - date_aux_end

                duration_reduce = (days * duration_recude_hours_default) + duration_recude_hours_start +duration_reduce_hours_end
                duration_standard = total_duration - duration_reduce


        return { 'minutes_standard': duration_standard.seconds//60 + duration_standard.days*1440, 'minutes_reduce':duration_reduce.seconds//60 + (duration_standard.seconds//60)%60 + duration_reduce.days*1440}
