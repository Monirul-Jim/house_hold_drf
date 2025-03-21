from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
# Create your models here.
User = get_user_model()


class Service(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='CartItem')

    def total_price(self):
        return sum(item.service.price for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         self.total_price = sum(
#             service.price for service in self.services.all())
#         super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='OrderItem')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Override save method to calculate total price from the user's cart."""
        if not self.pk:  # Only when creating a new order
            cart = Cart.objects.get(user=self.user)
            self.total_price = cart.total_price()
            super().save(*args, **kwargs)  # Save order first to get a primary key
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(order=self, service=cart_item.service)
            cart.services.clear()  # Clear the cart after creating an order
        else:
            super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.service.name} - {self.rating}/5'


class AdminManager(models.Manager):
    def promote_to_admin(self, user):
        user.is_staff = True
        user.is_superuser = True
        user.save()


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    @property
    def profile_picture(self):
        """
        Retrieve the profile picture of the client if it exists.
        """
        profile_image = self.clients.first()
        return profile_image.profile_picture.url if profile_image else None


class ClientProfileImage(models.Model):
    client_profile = models.ForeignKey(
        ClientProfile, on_delete=models.CASCADE, related_name='clients')
    profile_picture = CloudinaryField('image')
