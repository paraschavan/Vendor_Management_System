import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Vendor(models.Model):
    """
    Vendor Model
    This model stores essential information about each vendor and their performance metrics.
    Fields:
    - user: OneToOneField - Vendor's Authentication.
    - name: CharField - Vendor's name.
    - contact_details: TextField - Contact information of the vendor.
    - address: TextField - Physical address of the vendor.
    - vendor_code: CharField - A unique identifier for the vendor.
    - on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
    - quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
    - average_response_time: FloatField - Average time taken to acknowledge purchase orders.
    - fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.
    """

    def default_vendor_code():
        return str(uuid.uuid4().hex)[:10].upper()

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, unique=True, default=default_vendor_code,
                                   editable=False)  # Change to models.UUIDField
    on_time_delivery_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    quality_rating_avg = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    average_response_time = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fulfillment_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.vendor_code + ' - ' + self.name


class PurchaseOrder(models.Model):
    """
    Purchase Order (PO) Model
    This model captures the details of each purchase order and is used to calculate various performance metrics.
    Fields:
    - po_number: CharField - Unique number identifying the PO.
    - vendor: ForeignKey - Link to the Vendor model.
    - order_date: DateTimeField - Date when the order was placed.
    - actual_delivery_date: DateTimeField - Actual delivery date of the order.
    - expected_delivery_date: DateTimeField - Expected delivery date of the order.
    - items: JSONField - Details of items ordered.
    - quantity: IntegerField - Total quantity of items in the PO.
    - status: CharField - Current status of the PO (e.g., pending, completed, canceled).
    - quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
    - issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
    - acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.
    """

    def default_items():
        return {"data": {}}

    def default_po_number():
        return str(uuid.uuid4().hex)[:20].upper()

    po_number = models.CharField(max_length=20, unique=True, default=default_po_number,
                                 editable=False)  # Change to models.UUIDField
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(default=default_items)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('process', 'In Process'),
        ('completed', 'Completed'),
        ('return', 'Return'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name} - {self.status}"


class HistoricalPerformance(models.Model):
    """
    Historical Performance Model
    This model optionally stores historical data on vendor performance, enabling trend analysis.
    Fields:
    - vendor: ForeignKey - Link to the Vendor model.
    - date: DateTimeField - Date of the performance record.
    - on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
    - quality_rating_avg: FloatField - Historical record of the quality rating average.
    - average_response_time: FloatField - Historical record of the average response time.
    - fulfillment_rate: FloatField - Historical record of the fulfillment rate.
    """

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    quality_rating_avg = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    average_response_time = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fulfillment_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
