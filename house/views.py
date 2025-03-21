import cloudinary
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import rest_framework
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service, Cart, Order, Review, ClientProfile, OrderItem, ClientProfileImage
from .serializers import ServiceSerializer, OrderSerializer, ReviewSerializer, ClientProfileSerializer, ClientProfileImageSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

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


# class ClientProfileImageUploadView(APIView):
#     # Correctly define serializer class
#     serializer_class = ClientProfileImageSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def get_queryset(self):
#         """
#         Retrieve the client profile image by using the image_id from kwargs
#         or filter by client_profile.
#         """
#         return ClientProfileImage.objects.filter(client_profile_id=self.kwargs['user_id'])

#     def post(self, request, user_id):
#         """
#         Handle image upload for the user with given user_id.
#         """
#         # Get the client profile object
#         client_profile = get_object_or_404(ClientProfile, user_id=user_id)

#         # # Check if a profile image already exists for this client
#         # existing_image = ClientProfileImage.objects.filter(
#         #     client_profile=client_profile).first()
#         # if existing_image:
#         #     return Response({"error": "Profile image already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         # Save new profile image
#         serializer = ClientProfileImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(client_profile=client_profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, user_id):
#         """
#         Retrieve and return the client's profile image if exists.
#         """
#         # Retrieve client profile image using `user_id`
#         client_profile = get_object_or_404(ClientProfile, user_id=user_id)
#         # Fetch the profile image for the given client profile
#         profile_image = self.get_queryset().first()

#         if not profile_image:
#             return Response({"error": "No profile image found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ClientProfileImageSerializer(profile_image)
#         return Response(serializer.data)


# class ClientProfileImageUploadView(APIView):
#     serializer_class = ClientProfileImageSerializer

#     def post(self, request, user_id):
#         """
#         Handle image upload and associate it with the user.
#         """
#         client_profile = get_object_or_404(ClientProfile, user_id=user_id)

#         # If there's already an image, delete the old one (optional)
#         existing_image = ClientProfileImage.objects.filter(
#             client_profile=client_profile).first()
#         if existing_image:
#             # Delete the old image from Cloudinary using its public_id
#             try:
#                 cloudinary.uploader.destroy(
#                     existing_image.profile_picture.public_id)
#             except Exception as e:
#                 return Response({"error": f"Error deleting old image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#             # Delete the old image record from the database
#             existing_image.delete()

#             # Optionally, update the ClientProfile model if needed
#             client_profile.profile_picture = None  # or set to an appropriate value
#             client_profile.save()

#         # Save the new image
#         serializer = ClientProfileImageSerializer(data=request.data)
#         if serializer.is_valid():
#             # Create a new image entry and update the client profile
#             client_profile_image = serializer.save(
#                 client_profile=client_profile)
#             # Update profile picture in client profile
#             client_profile.profile_picture = client_profile_image.profile_picture.url
#             client_profile.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ClientProfileImageUploadView(APIView):
    serializer_class = ClientProfileImageSerializer

    def post(self, request, user_id):
        """
        Handle image upload and associate it with the user.
        """
        client_profile = get_object_or_404(ClientProfile, user_id=user_id)

        # If there's already an image, delete the old one
        existing_image = ClientProfileImage.objects.filter(
            client_profile=client_profile).first()
        if existing_image:
            # Delete the old image from Cloudinary using its public_id
            try:
                cloudinary.uploader.destroy(
                    existing_image.profile_picture.public_id)
                print(
                    f"Deleted image from Cloudinary: {existing_image.profile_picture.public_id}")
            except Exception as e:
                return Response({"error": f"Error deleting old image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the old image record from the database
            existing_image.delete()

            # Optionally, reset the profile picture field on the ClientProfile model
            client_profile.profile_picture = None  # Reset the profile picture field to None
            client_profile.save()

        # Save the new image
        serializer = ClientProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new image entry and update the client profile
            client_profile_image = serializer.save(
                client_profile=client_profile)
            # Update profile picture in client profile
            client_profile.profile_picture = client_profile_image.profile_picture.url
            client_profile.save()
            print(
                f"Uploaded new image for user {user_id} at {client_profile.profile_picture}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
