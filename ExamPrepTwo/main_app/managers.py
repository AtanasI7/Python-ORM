from django.db.models import manager
from django.db.models import Count


class ProfileManager(manager.Manager):
    def get_regular_customers(self):
        return self.annotate(
            orders_count=Count('profile_orders')
        ).filter(orders_count__gt=2).order_by('-orders_count')