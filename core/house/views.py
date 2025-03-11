from rest_framework import status
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service, Cart, Order, Review, ClientProfile
from .serializers import ServiceSerializer, OrderSerializer, ReviewSerializer, ClientProfileSerializer
from django.contrib.auth import get_user_model

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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
