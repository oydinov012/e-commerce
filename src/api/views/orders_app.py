from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Cart, Order, OrderItem
from api.serializer.orders_app import CartSerializer, OrderSerializer


class CartListApiView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartCreateApiView(CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDeleteApiView(DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CreateOrderFromCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        address = request.data.get("address")
        phone_number = request.data.get("phone_number")

        if not address or not phone_number:
            return Response({"error": "Address and phone_number required"}, status=400)

        total_price = 0

        order = Order.objects.create(
            user=request.user,
            address=address,
            phone_number=phone_number,
            total_price=0
        )

        for item in cart_items:
            item_total = item.product.price * item.quantity
            total_price += item_total

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        order.total_price = total_price
        order.save()

        cart_items.delete()

        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "total_price": total_price
        })


class OrderListApiView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")