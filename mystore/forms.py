from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Product, Profile, Customer, Store, Category


class UserInfoForm(forms.ModelForm):

	def __init__():
		pass
			
		phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
		role = forms.ChoiceField(label="", widget=forms.Select(), required=True)
		address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=False)
		address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
		city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
		state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
		zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
		country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

		class Meta:
			model = Profile
			fields = ('phone', 'role', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')




class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'





class UpdateUserForm(UserChangeForm):

	# Hide Password stuff
	password = None
	# Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	phone = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

		# def save(self, commit=True):
		# 	user = super().save(commit=False)
		# 	if commit:
		# 		customer = Customer.objects.create(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'])
		# 		customer.save()
				
		# 	return user


	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

	

class SignUpForm(UserCreationForm):
	# # email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	# # first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	# # last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	# email = forms.EmailField(required=True)
	# phone = forms.CharField(required=True)

	# ROLE_CHOICES = (
	# 	('store', 'Store'),
	# 	('customer', 'Customer'),
	# )
	# # role = forms.ChoiceField(label="", widget=forms.Select(), required=True)
	# role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)
	# store_name = forms.CharField(required=True)

	# class Meta:
	# 	model = User
	# 	fields = ['username', 'email', 'password1', 'password2', 'role', 'phone']

	# if role == 'store':
	# 	fields = ['username', 'email', 'password1', 'password2', 'role', 'store name', 'phone']

	# def save(self, commit=True):
	# 	user = super().save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 		phone = self.cleaned_data['phone']
	# 		profile = Profile.objects.create(user=user, role=self.cleaned_data['role'])
	# 		profile.save()
	# 		# customer.phone = self.cleaned_data['phone']
	# 		# customer = Customer.objects.create(user=user, phone=self.cleaned_data['phone'])
	# 		# customer.save()
			
		# return user

	username = forms.CharField(max_length=100)
	email = forms.EmailField()
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	phone = forms.CharField(max_length=20)
    
    # Role field
	ROLE_CHOICES = (
		('', 'Select Role'),  # Placeholder choice
		('customer', 'Customer'),
		('store', 'Store'),
	)
	role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    # Conditional fields
	address = forms.CharField(max_length=255, required=False)
	store_name = forms.CharField(max_length=100, required=False)
	latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
	longitude = forms.FloatField(required=False, widget=forms.HiddenInput())

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'phone', 'role']

	def clean(self):
		cleaned_data = super().clean()
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")
		role = cleaned_data.get("role")
		
		if password1 and password2 and password1 != password2:
			self.add_error('password2', "Passwords do not match.")
		
		# Validation for role-specific fields
		if role == 'store' and not cleaned_data.get("store_name"):
			self.add_error('store_name', "Store name is required for store role.")
		if role == 'customer' and not cleaned_data.get("address"):
			self.add_error('address', "Address is required for customer role.")


class PostingProducts(forms.ModelForm):

	def __init__(self, *args, **kwargs):

		super(PostingProducts, self).__init__(*args, **kwargs)

		self.name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
		self.description = forms.CharField(label="", max_length=600, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))
		self.price = forms.DecimalField(label="", decimal_places=2, max_digits=6, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Price'}))
		# self.category = forms.ForeignKey(Category, on_delete=forms.CASCADE, default=1)
		# self.category = forms.CharField(label="")
		self.image = forms.ImageField(widget=forms.FileInput(attrs={"id" : "image_field", "style" : "height: 100px ; width : 100px ; "}))
		self.sale_price = forms.DecimalField(decimal_places=2, max_digits=6, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Price'}))


	class Meta:
		model = Product
		fields = ('name', 'description', 'image', 'price')

	# class Meta:
	# 	model = Product
	# 	fields = ['name', 'description', 'price', 'image', 'category', 'is_sale', 'sale_price']
	# 	widgets = {
	# 		'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
	# 		'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
	# 		'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
	# 		'image': forms.FileInput(attrs={'id': 'image_field'}),
	# 		'category': forms.Select(attrs={'class': 'form-control'}),
	# 		'is_sale': forms.CheckboxInput(),
	# 		'sale_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sale Price'}),
	# 	}

	# def __init__(self, *args, **kwargs):
	# 	super(PostingProducts, self).__init__(*args, **kwargs)
	# 	self.fields['category'].queryset = Category.objects.all()  # List all categories