from .views import Main, ProductDetailView, CategoryDetailView, CartView, AddToCartView, DeleteFromCartView, QuantityOfProductsView, CheckoutView, MakeOrderView, LoginView
from django.urls import path, include

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name = 'product_inf'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name = 'category_inf'),
    path('cart/', CartView.as_view(), name = 'cart'),
    path('add_to_cart/<str:slug>/', AddToCartView.as_view(), name = 'add_to_cart'),
    path('remove_from_cart/<str:slug>/', DeleteFromCartView.as_view(), name = 'remove_from_cart'),
    path('quantity_of_products/<str:slug>/', QuantityOfProductsView.as_view(), name = 'quantity_of_products'),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),
    path('make_order/', MakeOrderView.as_view(), name = 'make_order'),
    path('login/', LoginView.as_view(), name = 'login')
]
