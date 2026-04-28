from django.db import models
from orders.models import Order
# Create your models here.


class Payment(models.Model):
    METHOD_CHOICES = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("click", "Click"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id}"