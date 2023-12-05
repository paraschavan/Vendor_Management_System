from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Vendor, PurchaseOrder
from django.contrib.auth.models import User
from rest_framework import status
from api.serializers import VendorSerializer, PurchaseOrderSerializer
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"\nFailed: {func.__name__}")
            raise e
        else:
            print(f"\nPassed: {func.__name__}")

    return wrapper


class TestVendorViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test123")
        self.client = Client()
        self.client.login(username="test", password="test123")
        self.setUpVendor()

    def setUpVendor(self):
        self.vendor = Vendor.objects.create(user=self.user, name="test", contact_details="NA", address="NA",
                                            vendor_code="test1", on_time_delivery_rate=99.0, quality_rating_avg=4.6,
                                            average_response_time=73.0, fulfillment_rate=100.0)

    @log
    def test_vendor_list_GET(self):
        vendor_list_url = reverse("vendor_list")
        response = self.client.get(vendor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0])["user"], self.user.id)

    @log
    def test_vendor_list_POST(self):
        vendor_list_url = reverse("vendor_list")
        response = self.client.post(vendor_list_url, {"name": "testPost",
                                                      "contact_details": "NA",
                                                      "address": "NA"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(dict(response.data)["name"], "testPost")

    @log
    def test_vendor_detail_GET(self):
        vendor_detail_url = reverse("vendor_detail", kwargs={"pk": self.vendor.id})
        response = self.client.get(vendor_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, VendorSerializer(self.vendor).data)

    @log
    def test_vendor_detail_PUT(self):
        vendor_detail_url = reverse("vendor_detail", kwargs={"pk": self.vendor.id})
        response = self.client.put(vendor_detail_url, data={"name": "testPUT",
                                                            "contact_details": "cdPUT",
                                                            "address": "cdPUT"
                                                            },
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["name"], "testPUT")

    @log
    def test_vendor_detail_PATCH(self):
        vendor_detail_url = reverse("vendor_detail", kwargs={"pk": self.vendor.id})
        response = self.client.patch(vendor_detail_url, data={"name": "testPATCH"},
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)["name"], "testPATCH")

    @log
    def test_vendor_detail_DELETE(self):
        self.assertEqual(Vendor.objects.count(), 1)
        vendor_detail_url = reverse("vendor_detail", kwargs={"pk": self.vendor.id})
        response = self.client.delete(vendor_detail_url, data={"id": self.vendor.id},
                                      content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    @log
    def test_vendor_performance_GET(self):
        vendor_performance_url = reverse("vendor_performance", kwargs={"pk": self.vendor.id})
        response = self.client.get(vendor_performance_url, data={"id": self.vendor.id},
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), VendorSerializer(self.vendor).data)


class TestPurchaseOrder(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="test1", password="test123")
        self.user2 = User.objects.create_user(username="test2", password="test321")
        self.client = Client()
        self.client.login(username="test1", password="test123")
        self.setUpVendor()
        self.setUpPurchaseOrder()

    def setUpVendor(self):
        self.vendor1 = Vendor.objects.create(user=self.user1, name="test1", contact_details="NA", address="NA",
                                             vendor_code="test1", on_time_delivery_rate=99.0, quality_rating_avg=4.6,
                                             average_response_time=73.0, fulfillment_rate=100.0)

        self.vendor2 = Vendor.objects.create(user=self.user2, name="test2", contact_details="NA", address="NA",
                                             vendor_code="test2", on_time_delivery_rate=95.0, quality_rating_avg=3.9,
                                             average_response_time=123.0, fulfillment_rate=94.0)

    def setUpPurchaseOrder(self):
        self.purchaseOrder = PurchaseOrder.objects.create(
            vendor=self.vendor1,
            actual_delivery_date=timezone.now(),  # Set the actual delivery date
            expected_delivery_date=timezone.now() + timezone.timedelta(days=7),
            # Set the expected delivery date (7 days from now)
            items={"data": {"item1": 7, "item2": 7}},  # Example item details
            quantity=14,
            status="pending",  # Set the status
            quality_rating=5,  # Set the quality rating (if applicable)
            acknowledgment_date=timezone.now() + timezone.timedelta(seconds=30),
            # Set the acknowledgment date (if applicable)
        )
        self.purchaseOrder2 = PurchaseOrder.objects.create(
            vendor=self.vendor2,
            actual_delivery_date=timezone.now(),
            expected_delivery_date=timezone.now() + timezone.timedelta(days=7),
            items={"data": {"item1": 5, "item2": 10}},
            quantity=15,
            status="pending",
            quality_rating=4.5,
            acknowledgment_date=timezone.now() + timezone.timedelta(seconds=30),
        )

        self.purchaseOrder3 = PurchaseOrder.objects.create(
            vendor=self.vendor2,
            actual_delivery_date=timezone.now(),
            expected_delivery_date=timezone.now() + timezone.timedelta(days=7),
            items={"data": {"item1": 25, "item2": 10}},
            quantity=35,
            status="pending",
            quality_rating=4.5,
            acknowledgment_date=timezone.now() + timezone.timedelta(seconds=30),
        )

    @log
    def test_purchase_order_list_POST(self):
        purchase_order_list_url = reverse("purchase_order_list")
        data = {
            "vendor": self.vendor1.id,
            "actual_delivery_date": timezone.now(),
            "expected_delivery_date": timezone.now() + timezone.timedelta(days=7),
            "items": {"data": {"item1": 1, "item2": 2}},
            "quantity": 3,
            "status": "pending",
            "quality_rating": 4.5,
            "acknowledgment_date": timezone.now() + timezone.timedelta(seconds=30)
        }
        response = self.client.post(purchase_order_list_url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['vendor'], self.vendor1.id)
        self.assertEqual(response.data['items'], data['items'])

    @log
    def test_purchase_order_list_GET(self):
        purchase_order_list_url = reverse("purchase_order_list")
        response = self.client.get(purchase_order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), PurchaseOrderSerializer(self.purchaseOrder).data)

    @log
    def test_purchase_order_list_by_vendor_GET(self):
        purchase_order_list_url = reverse("purchase_order_list")
        response = self.client.get(purchase_order_list_url, data={"vendor": self.vendor2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), PurchaseOrderSerializer(self.purchaseOrder2).data)
        self.assertEqual(dict(response.data[1]), PurchaseOrderSerializer(self.purchaseOrder3).data)

    @log
    def test_purchase_order_detail_GET(self):
        purchase_order_detail_url = reverse("purchase_order_detail", kwargs={"pk": self.purchaseOrder.id})
        response = self.client.get(purchase_order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), PurchaseOrderSerializer(self.purchaseOrder).data)

    @log
    def test_purchase_order_detail_PUT(self):
        purchase_order_detail_url = reverse("purchase_order_detail", kwargs={"pk": self.purchaseOrder.id})
        response = self.client.put(purchase_order_detail_url, data=PurchaseOrderSerializer(self.purchaseOrder2).data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)['vendor'], PurchaseOrderSerializer(self.purchaseOrder2).data['vendor'])

    @log
    def test_purchase_order_detail_PATCH(self):
        purchase_order_detail_url = reverse("purchase_order_detail", kwargs={"pk": self.purchaseOrder.id})
        response = self.client.patch(purchase_order_detail_url,
                                     data={'items': {'data': {'item1': 5, 'item2': 5}}, "quantity": 10},
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)['items'], {'data': {'item1': 5, 'item2': 5}})
        self.assertEqual(dict(response.data)['quantity'], 10)

    @log
    def test_purchase_order_detail_DELETE(self):
        self.assertEqual(PurchaseOrder.objects.count(), 3)
        purchase_order_detail_url = reverse("purchase_order_detail", kwargs={"pk": self.purchaseOrder.id})
        response = self.client.delete(purchase_order_detail_url, data={"id": self.purchaseOrder.id}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    @log
    def test_purchase_order_acknowledge_PATCH(self):
        purchase_order_detail_url = reverse("purchase_order_acknowledge", kwargs={"pk": self.purchaseOrder.id})
        data = {"acknowledgment_date": timezone.now()}
        response = self.client.patch(purchase_order_detail_url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['acknowledgment_date'],
                         PurchaseOrderSerializer(PurchaseOrder.objects.get(id=self.purchaseOrder.id)).data[
                             'acknowledgment_date'])
