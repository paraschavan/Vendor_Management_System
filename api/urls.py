from django.urls import path
from .views import VendorList, VendorDetail, VendorPerformance, PurchaseOrderList, PurchaseOrderDetail, \
    PurchaseOrderAcknowledge

urlpatterns = [
    #    API Endpoints:
    #    - POST /api/vendors/: Create a new vendor.
    #    - GET /api/vendors/: List all vendors.
    #    - GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    #    - PUT /api/vendors/{vendor_id}/: Replace a vendor's details.
    #    - PATCH /api/vendors/{vendor_id}/: Update a vendor's details.
    #    - DELETE /api/vendors/{vendor_id}/: Delete a vendor.
    path('vendors/', VendorList.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', VendorDetail.as_view(), name='vendor_detail'),
    #    - GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.
    path('vendors/<int:pk>/performance/', VendorPerformance.as_view(), name='vendor_performance'),
    #    API Endpoints:
    #    - POST /api/purchase_orders/: Create a purchase order.
    #    - GET /api/purchase_orders/: List all purchase orders
    #    - GET /api/purchase_orders/?vendor=1: List all purchase orders filtered by vendor
    #    - GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    #    - PUT /api/purchase_orders/{po_id}/: Replace a purchase order.
    #    - PATCH /api/purchase_orders/{po_id}/: Update a purchase order.
    #    - DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
    path('purchase_orders/', PurchaseOrderList.as_view(), name='purchase_order_list'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetail.as_view(), name='purchase_order_detail'),
    #    - PATCH /api/purchase_orders/{po_id}/acknowledge/: for vendors to acknowledge
    path('purchase_orders/<int:pk>/acknowledge/', PurchaseOrderAcknowledge.as_view(),
         name='purchase_order_acknowledge'),
]
