from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from main.models import PurchaseOrder
from django.db import transaction


@receiver(pre_save, sender=PurchaseOrder)
@transaction.atomic
def copy_old_vendor_performance(sender, instance, **kwargs):
    action = set()
    try:
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)
    except PurchaseOrder.DoesNotExist:
        # The instance is being created, not updated
        action.add('cal_on_time_delivery_rate')
        action.add('cal_quality_rating_avg')
        action.add('cal_average_response_time')
        action.add('cal_fulfilment_rate')
        instance._action = set()

    else:
        if instance.status == 'completed' and old_instance.status != instance.status:
            action.add('cal_on_time_delivery_rate')
        if instance.status == 'completed' and old_instance.quality_rating != instance.quality_rating:
            action.add('cal_quality_rating_avg')
        if old_instance.acknowledgment_date != instance.acknowledgment_date:
            action.add('cal_average_response_time')
        if instance.status == 'completed' and old_instance.status != instance.status:
            action.add('cal_fulfilment_rate')

        instance._action = action


@receiver(post_save, sender=PurchaseOrder)
@transaction.atomic
def update_vendor_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    if kwargs.get('created', False):  # Check if a new PurchaseOrder is created
        # Perform logic when a new PO is created (e.g., increment total PO count)
        pass

    def cal_on_time_delivery_rate():
        # Update On-Time Delivery Rate when a PO status changes to 'completed'
        completed_purchases = vendor.purchaseorder_set.filter(status='completed')
        on_time_deliveries = completed_purchases.filter(actual_delivery_date__lte=instance.expected_delivery_date)
        vendor.on_time_delivery_rate = (on_time_deliveries.count() / completed_purchases.count()) * 100

    def cal_quality_rating_avg():
        # Update Quality Rating Average when a completed PO has a quality rating
        completed_purchases_with_rating = vendor.purchaseorder_set.filter(status='completed',
                                                                          quality_rating__isnull=False)
        vendor.quality_rating_avg = sum(
            i.quality_rating for i in completed_purchases_with_rating) / completed_purchases_with_rating.count()

    def cal_average_response_time():
        # Update Average Response Time when a PO is acknowledged by the vendor
        acknowledged_purchases = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        total_acknowledged_purchases = acknowledged_purchases.count()
        total_response_time = sum(
            (purchase.acknowledgment_date - purchase.issue_date).total_seconds() for purchase in acknowledged_purchases)
        vendor.average_response_time = (
                total_response_time / total_acknowledged_purchases) if total_acknowledged_purchases > 0 else 0

    def cal_fulfilment_rate():
        # Update Fulfilment Rate upon any change in PO status
        total_purchases = vendor.purchaseorder_set.count()
        fulfilled_purchases = vendor.purchaseorder_set.filter(status='completed')
        vendor.fulfillment_rate = ((fulfilled_purchases.count() / total_purchases) * 100) if total_purchases > 0 else 0

    if 'cal_on_time_delivery_rate' in instance._action:
        cal_on_time_delivery_rate()
    if 'cal_quality_rating_avg' in instance._action:
        cal_quality_rating_avg()
    if 'cal_average_response_time' in instance._action:
        cal_average_response_time()
    if 'cal_fulfilment_rate' in instance._action:
        cal_fulfilment_rate()
    # Save the updated vendor instance
    vendor.save()
