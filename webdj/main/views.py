from django.shortcuts import render
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction
from .models import Hooks, Rods, Coils, Cargo, Wobblers, Soft_baits, Spinners, Corbs_and_lines, Groundbaits_ozzles, Feeders, Leashes, Fishing_accessories, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryInfMixin, CartMixin
from .forms import OrderForm
from .utils import recalc_cart


class Main(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_dropdown()
        products = LatestProducts.objects.get_products_for_main_page(
                'hooks', 'rods', 'coils', 'cargo', 'wobblers', 'soft_baits', 'spinners', 
                'corbs_and_lines', 'groundbaits_ozzles', 'feeders', 'leashes', 'fishing_accessories'
            )
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'main/index.html', context)


class ProductDetailView(CartMixin, CategoryInfMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'hooks': Hooks,
        'rods': Rods,
        'coils': Coils,
        'cargo': Cargo,
        'wobblers': Wobblers,
        'soft_baits': Soft_baits,
        'spinners': Spinners,
        'corbs_and_lines': Corbs_and_lines,
        'groundbaits_ozzles': Groundbaits_ozzles,
        'feeders': Feeders,
        'leashes': Leashes,
        'fishing_accessories': Fishing_accessories
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)


    #model = Model
    #queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'main/product_inf.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context 

class CategoryDetailView(CartMixin, CategoryInfMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_inf.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context 
    
class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product, created = CartProduct.objects.get_or_create(user = self.cart.owner, cart = self.cart, content_type = content_type, object_id = product.id)
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Продукт успішно доданий до кошика')
        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_dropdown()
        context = {'cart': self.cart, 'categories': categories}
        return render(request, 'main/cart.html', context)

class DeleteFromCartView(CartMixin, View):
    def get(self,request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product = CartProduct.objects.get(user = self.cart.owner, cart = self.cart, content_type = content_type, object_id = product.id)
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Продукт успішно видалений з кошика')
        return HttpResponseRedirect('/cart/')

class QuantityOfProductsView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product = CartProduct.objects.get(user = self.cart.owner, cart = self.cart, content_type = content_type, object_id = product.id)
        quantity = int(request.POST.get('quantity'))
        cart_product.number = quantity
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'К-ть продукту змінена')
        return HttpResponseRedirect('/cart/')

class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_dropdown()
        form = OrderForm(request.POST or None)
        context = {'cart': self.cart, 'categories': categories, 'form': form}
        return render(request, 'main/checkout.html', context)

class MakeOrderView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user = request.user)
        if form.is_valid():
            new_order = form.save(commit = False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying = form.cleaned_data['buying']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Замовлення успішно прийняте! Через деякий час вам зателефонують для підтвердження замовлення.')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')