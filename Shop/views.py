from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product,Cart, OrderPlaced, BannerImg,PaymentInfo
from .forms import UserRegistration, UserPasswordChange,CustomerProfile
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class ProductView(View):
    def get(self, request):
        totalitem = 0
        man = Product.objects.filter(category = 'm')
        woman = Product.objects.filter(category = 'w')
        kids = Product.objects.filter(category = 'k')
        payment_info = PaymentInfo.objects.all()
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Shop/home.html', {'man':man,'woman':woman,'kids':kids,'pay':payment_info,'totalitem':totalitem})


#class ProductDetailView(View):
  #def get(self,request, pk):
    #product = Product.objects.get(pk=pk)
    #return render(request, 'Shop/productdetail.html',{'product': product})
  
class ProductDetailView(View):
   def get(self,request,pk):
      product = Product.objects.get(pk=pk)
      item_already_in_cart = False
      totalitem = 0
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
      if request.user.is_authenticated:
         item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
      return render(request,'Shop/productdetail.html',{'product':product,'item_exist':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
   if request.user.is_authenticated:
      user = request.user
      amount = 0.0
      shipping_cost = 100.0
      total_amount = 0.0
      totalitem = 0
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
         for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_cost
         cart = Cart.objects.filter(user=user)
         return render(request, 'Shop/addtocart.html',{'carts':cart,'amount':amount,'total_amount':total_amount,'shipping_cost':shipping_cost,'totalitem':totalitem})
      else:
         totalitem = 0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
         return render(request,'Shop/emptycart.html',{'totalitem':totalitem})

@login_required
def buy_now(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/checkout')

@login_required
def plus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity += 1
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.product.discounted_price)
         amount += tempamount
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

@login_required
def minus_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity -= 1
      if Cart.objects.get(Q(product=prod_id)):
         if c.quantity == 0:
            print(c)
            c.delete()
            amount = 0.0
            shipping_amount = 100.0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)
         else:
            print(c.quantity)
      c.save()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.product.discounted_price)
         amount += tempamount
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

@login_required  
def remove_cart(request):
   if request.method=='GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0.0
      shipping_amount = 100.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         tempamount = (p.quantity * p.product.discounted_price)
         amount += tempamount
      data = {
         'amount':amount,
         'totalamount': amount + shipping_amount
            }
      return JsonResponse(data)

#profile
@method_decorator(login_required,name='dispatch')
class profile(View):
   def get(self,request):
      totalitem = 0
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
      form = CustomerProfile()
      return render(request, 'Shop/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
   def post(self,request):
      form = CustomerProfile(request.POST)
      totalitem = 0
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         division = form.cleaned_data['division']
         district = form.cleaned_data['district']
         thana = form.cleaned_data['thana']
         villorroad = form.cleaned_data['villorroad']
         zipcode = form.cleaned_data['zipcode']

         data = Customer(user=usr,name=name,division=division,district=district,thana=thana,villorroad=villorroad,zipcode=zipcode)
         data.save()
         messages.success(request,'Profile Updated Successfully!')
      return render(request,'Shop/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 totalitem = 0
 if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'Shop/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user= request.user)
 totalitem = 0
 if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'Shop/orders.html',{'orders':op,'totalitem':totalitem})

def man(request, data =None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        man = Product.objects.filter(category = 'm')
    elif data == 'sprint' or data == 'apex':
        man = Product.objects.filter(category='m').filter(brand=data)
    elif data == 'below':
        man = Product.objects.filter(category='m').filter(discounted_price__lt=3000)
    elif data == 'above':
        man = Product.objects.filter(category='m').filter(discounted_price__gt=3000)
    return render(request, 'Shop/man.html', {'man':man,'totalitem':totalitem})

def woman(request, data =None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        woman = Product.objects.filter(category = 'w')
    elif data == 'sprint' or data == 'ninorossi':
        woman = Product.objects.filter(category='w').filter(brand=data)
    elif data == 'below':
        woman = Product.objects.filter(category='w').filter(discounted_price__lt=2000)
    elif data == 'above':
        woman = Product.objects.filter(category='w').filter(discounted_price__gt=3000)
    return render(request, 'Shop/woman.html', {'woman':woman,'totalitem':totalitem})

def kids(request, data =None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        kid = Product.objects.filter(category = 'k')
    elif data == 'boy' or data == 'girl':
        kid = Product.objects.filter(category='k').filter(brand=data)
    elif data == 'below':
        kid = Product.objects.filter(category='k').filter(discounted_price__lt=1000)
    elif data == 'above':
        kid = Product.objects.filter(category='k').filter(discounted_price__gt=1000)
    return render(request, 'Shop/kids.html', {'kid':kid,'totalitem':totalitem})

def gift_card(request):
   totalitem = 0
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   gifts = Product.objects.filter(category='g')
   return render(request,'Shop/gift.html',{'gifts':gifts,'totalitem':totalitem})

class UserRegistrationView(View):
   def get(self,request):
      form = UserRegistration()
      return render(request, 'Shop/customerregistration.html',{'form':form})
   def post(self,request):
      form = UserRegistration(request.POST)
      if form.is_valid():
         messages.success(request,"A new user created!!")
         form.save()
      return render(request,'Shop/customerregistration.html',{'form':form}) 

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user = user)
 cart_items = Cart.objects.filter(user = user)
 amount = 0.0
 shipping_amount = 100.0
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    totalamount = amount + shipping_amount
 return render(request, 'Shop/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer.objects.get(id=custid)
   cart = Cart.objects.filter(user = user)
   for c in cart:
      OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
      c.delete()
   return redirect('/orders')

def search(request):
   if request.method == 'GET':
      query = request.GET.get('quary')
      if query:
         # product = Product.objects.filter(title__icontains = query)
         if Product.objects.filter(title__icontains = query).exists():
            product = Product.objects.filter(title__icontains = query)
            return render(request,'Shop/search.html',{'product':product})
         else:
            print('Product not available.')
            messages.success(request,'Product not available.')
            return render(request,'Shop/search.html')
      else:
         return redirect('/')
