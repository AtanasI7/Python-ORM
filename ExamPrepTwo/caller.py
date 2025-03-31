import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, Max, F, Case, When, Value


def get_profiles(search_string: str=None) -> str:
    if search_string is None:
        return ""

    profiles = Profile.objects.prefetch_related('profile_orders').filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).annotate(
        orders_count=Count('profile_orders')
    ).order_by('full_name')

    result = []

    for p in profiles:
        result.append(f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders_count}')

    return '\n'.join(result)

def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if profiles is None:
        return ""

    return '\n'.join(f"Profile: {p.full_name}, orders: {p.orders_count}" for p in profiles)

def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').order_by('products__name').last()

    if last_order is None or not last_order.products:
        return ""

    product_names = [p.name for p in last_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products() -> str:
    products = Product.objects.prefetch_related('product_orders').annotate(
        product_times_ordered=Count('product_orders')
    ).filter(product_times_ordered__gt=0).order_by('-product_times_ordered', 'name')[:5]

    if not products.exists():
        return ""

    result = ["Top products:"]

    for p in products:
        result.append(f"{p.name}, sold {p.product_times_ordered} times")

    return '\n'.join(result)

def apply_discounts() -> str:
    orders = Order.objects.prefetch_related('products').annotate(
        ordered_products = Count('products')
    ).filter(
        ordered_products__gt=2,
        is_completed=False
    )

    updated_orders_count = orders.update(total_price=F('total_price') * 0.90)

    return f"Discount applied to {updated_orders_count} orders."

def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if order is None:
        return ""

    Product.objects.filter(order=order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('in_available')
        )
    )

    order.is_completed = True
    order.save()

    # for p in order.products.all():
    #     Product.objects.filter(name=p.name).update(in_stock=F('in_stock') - p.product_count)
    #
    #     if p.in_stock == 0:
    #         p.is_available = False
    #
    # order.save()

    return f"Order has been completed!"






















