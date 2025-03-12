from rest_framework import status
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service, Cart, Order, Review, ClientProfile, OrderItem
from .serializers import ServiceSerializer, OrderSerializer, ReviewSerializer, ClientProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response({'services': [service.name for service in cart.services.all()]})

    def add_service(self, request, service_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        service = Service.objects.get(id=service_id)
        cart.services.add(service)
        return Response({'message': 'Service added to cart'})

    def remove_service(self, request, service_id):
        cart = Cart.objects.get(user=request.user)
        service = Service.objects.get(id=service_id)
        cart.services.remove(service)
        return Response({'message': 'Service removed from cart'})


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         user = self.request.user
#         cart = Cart.objects.get(user=user)
#         order = Order.objects.create(user=user, total_price=cart.total_price())
#         for cart_item in cart.cartitem_set.all():
#             OrderItem.objects.create(order=order, service=cart_item.service)
#         cart.services.clear()  # Empty the cart after order placement
#         return order
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure that only orders for the logged-in user are shown
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        # Ensure the user has a cart with services
        cart = Cart.objects.get(user=user)
        if cart.cartitem_set.exists():
            order = serializer.save(user=user, total_price=cart.total_price())
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order, service=cart_item.service)
            cart.services.clear()  # Clear cart after order placement
        else:
            raise serializers.ValidationError("Your cart is empty!")


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdminPromotionView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return Response({'message': 'User promoted to admin'})


class ClientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = ClientProfile.objects.get_or_create(
            user=request.user)
        serializer = ClientProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = ClientProfile.objects.get(user=request.user)
        serializer = ClientProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
