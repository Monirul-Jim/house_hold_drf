from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
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
    services = models.ManyToManyField(Service)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total_price before saving
        if self.pk:  # If order already exists
            self.total_price = sum(
                service.price for service in self.services.all())
        super().save(*args, **kwargs)


# 🔥 Automatically update total_price when services change in an order
@receiver(m2m_changed, sender=Order.services.through)
def update_total_price(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.total_price = sum(
            service.price for service in instance.services.all())
        instance.save()


# 🔥 Auto-create an order when a cart is updated
@receiver(m2m_changed, sender=Cart.services.through)
def create_order_from_cart(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        # Check if an order already exists for this cart
        order, created = Order.objects.get_or_create(user=instance.user)

        # Sync services from the cart to the order
        order.services.set(instance.services.all())

        # Update total price
        order.total_price = sum(
            service.price for service in order.services.all())
        order.save()


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
    profile_picture = models.ImageField(
        upload_to='profile_picture/', blank=True, null=True)
    social_media_links = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
