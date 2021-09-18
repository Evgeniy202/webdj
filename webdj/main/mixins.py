from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Category, Cart, Customer, Hooks, Rods, Coils, Cargo, Wobblers, Soft_baits, Spinners, Corbs_and_lines, Groundbaits_ozzles, Feeders, Leashes, Fishing_accessories

class CategoryInfMixin(SingleObjectMixin):

	CATEGORY_SLUG_TO_PRODUCT_MODEL = {
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

	def get_context_data(self, **kwargs):
		if isinstance(self.get_object(), Category):
			model = self.CATEGORY_SLUG_TO_PRODUCT_MODEL[self.get_object().slug]
			context = super().get_context_data(**kwargs)
			context['categories'] = Category.objects.get_categories_for_dropdown()
			context['category_products'] = model.objects.all()
			return context
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.get_categories_for_dropdown()
		return context

class CartMixin(View):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			customer = Customer.objects.filter(user = request.user).first()
			if not customer:
				customer = Customer.objects.create(user = request.user) 
			cart = Cart.objects.filter(owner = customer, in_order = False).first()
			if not cart:
				cart = Cart.objects.create(owner = customer)
		else:
			cart = Cart.objects.filter(for_anonymous_user = True).first()
			if not cart:
				cart = Cart.objects.create(for_anonymous_user = True)
		self.cart = cart
		return super().dispatch(request, *args, **kwargs)