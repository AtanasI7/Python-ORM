import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Sum, Q, F


def product_quantity_ordered():
    orders = Product.objects.annotate(
        total_quantity=Sum('orderproduct__quantity')
    ).exclude(
        total_quantity=None
    ).values(
        'name', 'total_quantity'
    ).order_by(
        '-total_quantity'
    )
    return '\n'.join(f"Quantity ordered of {o['name']}: {o['total_quantity']}" for o in orders)

def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set').order_by('id')
    result = []

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        ordered_products = order.orderproduct_set.all()

        for ordered_product in ordered_products:
            result.append(f'- Product: {ordered_product.product.name}, Category: {ordered_product.product.category.name}')

    return '\n'.join(result)

def filter_products():
    products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by('-price', 'name')
    result = []

    for p in products:
        result.append(f'{p.name}: {p.price}lv.')

    return '\n'.join(result)

def give_discount():
    Product.objects.filter(is_available=True, price__gt=3.00).update(price=F('price') * 0.7)
    available_products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    return '\n'.join(f"{p.name}: {p.price}lv." for p in available_products)












