from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Record_model
from .serializer import Record_serializer

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record_model.objects.all()
    serializer_class =  Record_serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
