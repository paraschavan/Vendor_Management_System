from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Vendor, PurchaseOrder, HistoricalPerformance
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f'\nFailed: {func.__name__}')
            raise e
        else:
            print(f'\nPassed: {func.__name__}')

    return wrapper


class VendorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='test123')
        self.vendor = Vendor.objects.create(
            user=self.user,
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )

    @log
    def test_vendor_str_method(self):
        self.assertEqual(str(self.vendor), f"{self.vendor.vendor_code} - {self.vendor.name}")


class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='test123')
        self.vendor = Vendor.objects.create(
            user=self.user,
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            quantity=100,
            status='pending',
            quality_rating=4.0
        )

    @log
    def test_purchase_order_str_method(self):
        expected_str = f"{self.purchase_order.po_number} - {self.vendor.name} - {self.purchase_order.status}"
        self.assertEqual(str(self.purchase_order), expected_str)

    @log
    def test_purchase_order_defaults(self):
        self.assertEqual(self.purchase_order.status, 'pending')
        self.assertIsNotNone(self.purchase_order.issue_date)
        self.assertIsNone(self.purchase_order.actual_delivery_date)
        self.assertIsNone(self.purchase_order.expected_delivery_date)


class HistoricalPerformanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='test123')
        self.vendor = Vendor.objects.create(
            user=self.user,
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )
        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.0,
            average_response_time=3.0,
            fulfillment_rate=95.0
        )

    @log
    def test_historical_performance_str_method(self):
        expected_str = f"{self.vendor.name} - {self.historical_performance.date}"
        self.assertEqual(str(self.historical_performance), expected_str)
