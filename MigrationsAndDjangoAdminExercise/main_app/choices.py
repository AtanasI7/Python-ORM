from django.db import models


class OrderStatusChoices(models.TextChoices):
    PENDING = 'P', 'Pending'
    COMPLETED = "CMD", "Completed"
    CANCELLED = "CAN", "Cancelled"