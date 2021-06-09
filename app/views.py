from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import  login_required
from django.utils.decorators import method_decorator

#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  totalitem=0
  topwear = Product.objects.filter(category='TW')
  bottomwear = Product.objects.filter(category='BW')
  mobile = Product.objects.filter(category='M')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html', {'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile, 'totalitem':totalitem})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class product_detail(View):
 def get(self,request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
   item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 totalitem=0
 if request.user.is_authenticated:
  user= request.user
  cart= Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount=70.0
  cart_product=[p for p in Cart.objects.all() if p.user==user]

  if cart_product:
   for p in cart_product:
    temp_amount=(p.quantity * p.product.discounted_price)
    amount += temp_amount
    tot_amount= amount + shipping_amount
    if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'app/addtocart.html', {'carts':cart, 'tot_amount':tot_amount, 'amount':amount, 'totalitem':totalitem})
  else:
    return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method =='GET':
  prod_id =request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity +=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount


  data={
   'quantity': c.quantity,
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)

def minus_cart(request):
 if request.method =='GET':
  prod_id =request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount

  data={
   'quantity': c.quantity,
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)

@login_required
def remove_cart(request):
 if request.method =='GET':
  prod_id =request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount

  data={
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 addr = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'addr':addr, 'active':'btn-primary'})

@login_required
def orders(request):
 totalitem=0
 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})


def mobile(request, data=None):
 totalitem = 0
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'iphone' or data == 'samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=35000)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=35000)

 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))

 return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})

def laptop(request, data=None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'mac' or data == 'hp':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)

 return render(request, 'app/laptop.html', {'laptops':laptops})

def topwear(request, data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)

 return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request, data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=500)

 return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Conggratulations .!! succesfully registered.')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 totalamount = 0.0
 shipping_amount = 70.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
   totalamount = amount + shipping_amount

 return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalamount':totalamount})

@login_required
def paymentdone(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect ("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active': 'btn-primary'})

 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name= form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   zipcode = form.cleaned_data['zipcode']
   state = form.cleaned_data['state']
   city = form.cleaned_data['city']
   reg = Customer(user=usr, name=name, locality=locality, zipcode=zipcode,state=state,city=city)
   reg.save()
   messages.success(request, 'congratz.!! profile updated successfully')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


