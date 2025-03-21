from django.contrib import admin
from .models import Service, Cart, CartItem, Order, Review, ClientProfile

# Register the Service model


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

# Register the Cart model


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price']
    search_fields = ['user__email']  # Search by user email
    readonly_fields = ['total_price']

# Register the CartItem model


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'service', 'created_at']
    search_fields = ['cart__user__email', 'service__name']
    list_filter = ['created_at']

# Register the Order model


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['total_price']

# Register the Review model


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'rating', 'created_at']
    search_fields = ['user__email', 'service__name']
    list_filter = ['rating', 'created_at']

# Register the ClientProfile model


# @admin.register(ClientProfile)
# class ClientProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'bio']
#     search_fields = ['user__email']
#     readonly_fields = ['user']
@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    # Add profile picture to list display
    list_display = ['user', 'bio', 'profile_picture_display']
    search_fields = ['user__email']
    readonly_fields = ['user']

    def profile_picture_display(self, obj):
        """
        Display the profile picture URL in the admin list view.
        """
        # If profile_picture exists, return the URL, otherwise show 'No image'
        if obj.profile_picture:
            return obj.profile_picture
        return "No image"

    # Set column name for the admin list
    profile_picture_display.short_description = 'Profile Picture URL'
