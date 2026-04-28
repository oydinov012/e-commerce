from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from payments.models import Payment


class MockPaymentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        method = request.data.get("method", "cash")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.total_price,
            is_paid=True
        )

        order.status = "paid"
        order.save()

        return Response({
            "message": "Payment successful",
            "payment_id": payment.id,
            "amount": payment.amount,
            "method": payment.method
        })