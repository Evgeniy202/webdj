from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
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

class SignupForm(forms.ModelForm):

	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput)
	passwordconf = forms.CharField(widget=forms.PasswordInput)
	phone = forms.CharField(required=False)
	address = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логін'
		self.fields['email'].label = 'Електронна пошта'
		self.fields['password'].label = 'Пароль'
		self.fields['passwordconf'].label = 'Будьласка підтвердіть пароль'
		self.fields['first_name'].label = "Ім'я"
		self.fields['last_name'].label = 'Прізвище'
		self.fields['phone'].label = 'Телефон'
		self.fields['address'].label = 'Адреса'

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(f'Даний електронний адрес вже зареєстрованно в ситемі!')
		return email

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(f'Логін "{username}" вже зайнятий! Спробуйте ввести інший логін.')
		return username

	def clean(self):
		password = self.cleaned_data['password']
		passwordconf = self.cleaned_data['passwordconf']
		if password != passwordconf:
			raise forms.ValidationError(f'Пароль не збігається! Спробуйте ще.')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'passwordconf', 'first_name', 'last_name', 'phone', 'address']	