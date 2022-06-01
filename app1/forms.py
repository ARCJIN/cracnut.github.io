from django.forms import ModelForm
from .models import *



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['mode_of_payment']

class AddCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name','username','password' , 'email' , 'phone', 'address','profile_image']



class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['profile_image','desc']
