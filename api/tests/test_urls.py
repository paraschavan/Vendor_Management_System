from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import VendorList, VendorDetail, VendorPerformance, PurchaseOrderList, PurchaseOrderDetail, \
    PurchaseOrderAcknowledge
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


class TestUrls(SimpleTestCase):

    @log
    def test_vendor_list_url_resolves(self):
        url = reverse('vendor_list')
        self.assertEqual(resolve(url).func.view_class, VendorList)

    @log
    def test_vendor_detail_url_resolves(self):
        url = reverse('vendor_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, VendorDetail)

    @log
    def test_vendor_performance_url_resolves(self):
        url = reverse('vendor_performance', args=[1])
        self.assertEqual(resolve(url).func.view_class, VendorPerformance)

    @log
    def test_purchase_order_list_url_resolves(self):
        url = reverse('purchase_order_list')
        self.assertEqual(resolve(url).func.view_class, PurchaseOrderList)

    @log
    def test_purchase_order_detail_url_resolves(self):
        url = reverse('purchase_order_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, PurchaseOrderDetail)

    @log
    def test_purchase_order_acknowledge_update_url_resolves(self):
        url = reverse('purchase_order_acknowledge', args=[1])
        self.assertEqual(resolve(url).func.view_class, PurchaseOrderAcknowledge)
