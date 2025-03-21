
from rest_framework import serializers
from .models import Service, Order, Review, ClientProfile, ClientProfileImage
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):
#     # total_price = serializers.ReadOnlyField()

#     class Meta:
#         model = Order
#         fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    # Make sure it uses ServiceSerializer
    services = ServiceSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'services', 'total_price', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# class ClientProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientProfile
#         fields = '__all__'
class ClientProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = ClientProfile
        fields = ['id', 'user', 'bio', 'social_media_links', 'profile_picture']

    def get_profile_picture(self, obj):
        # You can directly return the URL or `None` if no image exists
        return obj.profile_picture


class ClientProfileImageSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = ClientProfileImage
        fields = ['id', 'profile_picture']
