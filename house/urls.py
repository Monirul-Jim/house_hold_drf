from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, CartViewSet, OrderViewSet, ReviewViewSet, AdminPromotionView, ClientProfileView, ClientProfileImageUploadView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = router.urls + [
    path('cart/add/<int:service_id>/',
         CartViewSet.as_view({'post': 'add_service'}), name='add-to-cart'),
    path('cart/remove/<int:service_id>/',
         CartViewSet.as_view({'delete': 'remove_service'}), name='remove-from-cart'),
    path('promote-admin/', AdminPromotionView.as_view(), name='promote-admin'),
    path('client-profile/', ClientProfileView.as_view(), name='client-profile'),
    path('client-profile/<int:user_id>/image/',
         ClientProfileImageUploadView.as_view(), name='upload-profile-image'),
]
