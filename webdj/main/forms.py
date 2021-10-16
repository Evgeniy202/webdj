from django import forms
from django.contrib.auth.models import User
from .models import Order


class OrderForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['order_date'].label = 'Дата отримання замовлення'
		self.fields['buying'].label = 'Отримання замовлення'

	order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

	class Meta:
		model = Order
		fields = ('first_name', 'last_name', 'phone', 'address', 'buying', 'order_date', 'comment')

class LoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.fields['username'].label = 'Логін'
	    self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username = username).exists():
			raise forms.ValidationError(f'Користувач "{username}" не існує!')
		user = User.objects.filter(username = username).first()
		if user:
			if not user.check_password(password):
				raise forms.ValidationError('Невірний пароль!')
		return self.cleaned_data	

	class Meta:
		model = User
		fields = ['username', 'password']	