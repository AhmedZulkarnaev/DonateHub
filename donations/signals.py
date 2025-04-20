from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from django.db.models import Sum


@receiver(post_save, sender=Payment)
def update_collect_stats_on_payment(sender, instance, created, **kwargs):
    if not created:
        return

    collect = instance.collect
    total_amount = collect.payments.aggregate(
        total=Sum('amount')
    )['total'] or 0
    unique_donators = collect.payments.values('donator').distinct().count()

    collect.collected_amount = total_amount
    collect.donators_count = unique_donators
    collect.save()
