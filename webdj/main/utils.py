from django.db import models


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('general_price'), models.Count('id'))
    if cart_data.get('general_price__sum'):
        cart.general_price = cart_data['general_price__sum']
    else:
        cart.general_price = 0
    cart.general_products = cart_data['id__count']
    cart.save()
