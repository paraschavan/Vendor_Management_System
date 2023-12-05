from rest_framework import serializers
from main.models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    # Make Some Fields Read Only
    on_time_delivery_rate = serializers.FloatField(read_only=True)
    quality_rating_avg = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    fulfillment_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'


class VendorPerformanceSerializer(serializers.ModelSerializer):
    # Make Some Fields Read Only
    on_time_delivery_rate = serializers.FloatField(read_only=True)
    quality_rating_avg = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    fulfillment_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('acknowledgment_date',)

# class HistoricalPerformanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HistoricalPerformance
#         fields = '__all__'
