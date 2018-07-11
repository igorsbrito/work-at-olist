from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Record_model
from .serializer import Record_serializer

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record_model.objects.all()
    serializer_class =  Record_serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        data= request.data

        # if the call data is a end record,
        if data['type'] == '1':
            #check if exist a start call record with the same call id
            if(self.exists_start_call(data['call_id'])):

                #check if this data record is already registered
                if(self.exists_end_call(data['call_id'])):
                    return Response({'msg': 'Call end is already recorded'}, status=status.HTTP_400_BAD_REQUEST)

                Record_model.objects.create(call_id=data['call_id'],
                                            type=data['type'],
                                            timestamp=data['timestamp'])

                #create a bill record for this call
                #TO DO:

            else:
                return Response({'msg': 'this call id doesn`t have a start record'}, status=status.HTTP_400_BAD_REQUEST)
        #if the call data is a start record
        else:

            #check if this data record is already registered
            if(self.exists_start_call(data['call_id'])):
                return Response({'msg':'Call start is already recorded'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Record_model.objects.create(call_id=data['call_id'],
                                            type=data['type'],
                                            timestamp=data['timestamp'],
                                            source=data['source'],
                                            destination=data['destination'])

        return Response(status=status.HTTP_201_CREATED)


    def exists_start_call(self, call_id):
        records = Record_model.objects.filter(call_id=call_id, type=0)

        if (len(records) > 0):
            return True
        else:
            return False

    def exists_end_call(self, call_id):
        records = Record_model.objects.filter(call_id=call_id, type=1)

        if (len(records) > 0):
            return True
        else:
            return False