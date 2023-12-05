from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from main.models import Vendor, PurchaseOrder
from api.serializers import VendorSerializer, VendorPerformanceSerializer, PurchaseOrderSerializer, \
    PurchaseOrderAcknowledgeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import PurchaseOrderFilter
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsVendor


# Create your views here.

class VendorList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer

    def get_queryset(self):
        # Get the vendor ID from the URL parameter
        vendor_id = self.kwargs['pk']
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        return Vendor.objects.filter(pk=vendor.id)


class VendorPerformance(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VendorPerformanceSerializer

    def get_queryset(self):
        # Get the vendor ID from the URL parameter
        vendor_id = self.kwargs['pk']
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        return Vendor.objects.filter(pk=vendor.id)


class PurchaseOrderList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PurchaseOrderFilter


class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderAcknowledge(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsVendor]

    def patch(self, request, pk):
        instance = PurchaseOrder.objects.get(pk=pk)
        if instance.vendor.user != request.user:
            return JsonResponse({"msg": "Can't Acknowledge Other Vendor PO", }, status=403)
        instance.acknowledgment_date = timezone.now()
        instance.save()
        serializer = PurchaseOrderAcknowledgeSerializer(instance)
        return JsonResponse(data={"data":serializer.data}, status=200)
