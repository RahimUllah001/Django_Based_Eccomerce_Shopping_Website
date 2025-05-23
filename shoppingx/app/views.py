from django.shortcuts import render,redirect
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q   
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator        #for class bases view


# For home we make class based view
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})
    
    
class ProductDetailView(View):
    
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    # The below Line  
    # Check if the item already exists in the cart
    # This line tries to find an existing Cart item for the given user and product.

    # ✅ If it exists, it returns that Cart item and sets created = False.

    # 🆕 If it doesn't exist, it creates a new Cart object with user and product, and sets created = True.
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Product quantity updated in cart.")
    else:
        messages.success(request, "Product added to cart.")

    return redirect("/cart")



@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0  
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
             
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':total_amount,'amount':amount,'shipping_amount':shipping_amount})
        else:
           return render(request,'app/emptycart.html')


def plus_cart(request):
    print("PROD ID:", request.GET.get('prod_id'))
    print("USER ID:", request.user)
    print("USER ID:", request.user.id)
    print("USER ID:", request.user.username)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                # total_amount = amount + shipping_amount
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount,
                'shipping_amount':shipping_amount
            }
            return JsonResponse(data)
        else:
            return render(request,'app/emptycart.html')
   

def minus_cart(request):
    print("PROD ID:", request.GET.get('prod_id'))
    print("USER ID:", request.user)
    print("USER ID:", request.user.id)
    print("USER ID:", request.user.username)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                # total_amount = amount + shipping_amount
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount,
                'shipping_amount':shipping_amount
            }
            return JsonResponse(data)
        else:
            return render(request,'app/emptycart.html')


def remove_cart(request):
    print("PROD ID:", request.GET.get('prod_id'))
    print("USER ID:", request.user)
    print("USER ID:", request.user.id)
    print("USER ID:", request.user.username)
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                # total_amount = amount + shipping_amount
            data = {
                'amount':amount,
                'totalamount':amount + shipping_amount,
                'shipping_amount':shipping_amount
            }
            return JsonResponse(data)
        else:
            return render(request,'app/emptycart.html')














def buy_now(request):
    return render(request, 'app/buynow.html')





# Endpoint for Address
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

# endpoint for orders
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op, 'active':'btn-primary'})

# endpoint for Mobile
def mobile(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Apple' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

# endpoint for topware
def topwear(request,data = None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Cutton' or data == 'Fabric':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)

    return render(request, 'app/topwear.html', {'topwears':topwears})
 



# Customer Registeration View
class CustomerRegistrationView(View):
    def get(self,request):
       form = CustomerRegistrationForm()
       return render(request, 'app/customerregistration.html',{'form':form})
   
    def post(self,request):
       form = CustomerRegistrationForm(request.POST)
       if form.is_valid():
        messages.success(request,'Congratulations!! Registered Successfully')
        form.save()
       return render(request,'app/customerregistration.html',{'form':form})
      
# Checkout
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalamount':total_amount,'amount':amount,})

# Payment Done Method
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart_items = Cart.objects.filter(user=user)
    for cart_item in cart_items:
        OrderPlaced(user=user, customer=customer, product=cart_item.product, quantity=cart_item.quantity).save()
        cart_item.delete()
    return redirect("orders")



@method_decorator(login_required, name='dispatch') 
class ProfileView(View):
    def get(self,request):
       form = CustomerProfileForm()
       return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
    
    def post(self,request):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
          usr = request.user
          name = form.cleaned_data['name']
          locality = form.cleaned_data['locality']
          city = form.cleaned_data['city']
          state = form.cleaned_data['state']
          zipcode = form.cleaned_data['zipcode']
          reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
          reg.save()
          messages.success(request,'Congratulations!! Profile Updated Successfully')
          
          return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})