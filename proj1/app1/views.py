from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
import razorpay
import hashlib
from adminservices.models import *
# from numpy import insert
from .models import *
from django.contrib.auth import logout
from random import *
import smtplib
from django.core.mail import send_mail
import os
import uuid
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        # pas = request.POST['password']

        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        pas = pwd.hexdigest()
        if User.objects.filter(email=email).exists():
            data = {
                "msg": "Email Address Is Already Register !!! "
            }
            return render(request, "webpages/sign_up.html", data)
        else:
            obj = User(fname=fname, lname=lname, email=email, password=pas)
            obj.save()
        return redirect('login')
    else:
        print('---- Registration Successfull ----')
    return render(request, "webpages/sign_up.html")


def login(request):
    
    if request.session.has_key('is_login'):
        return redirect('index')
    if request.POST:
        email = request.POST['email']
        # password = request.POST['password']
        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()

        count = User.objects.filter(email=email, password=password).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['email'] = email
            request.session['id'] = User.objects.values('id').filter(email=email, password=password)[0]['id']
            user = User.objects.get(id=request.session['id'])
            request.session['fname'] = user.fname
            return redirect('index')
        else:
            data = {
                "msg": "Email or Password Are Incorrect !!!"
            }
            return render(request, "webpages/login.html", data)

    else:
        print('login main error')
    return render(request, "webpages/login.html")

def user_logout(request):
    del request.session['is_login']
    return redirect('index')



def index(request):
    product = Product.objects.filter(subcatid='1')
    product1 = Product.objects.filter(subcatid='2')
    product2 = Product.objects.filter(subcatid='3')
    product3 = Product.objects.filter(subcatid='8')
    if request.session.has_key('is_login'):
        return render(request, "webpages/index.html",{'product':product,'product1':product1,'product2':product2,'product3':product3})
    return render(request, "webpages/index.html")


def show_profile(request):
    sesson_id = request.session.get('id')
    user = User.objects.get(id=sesson_id)
    data = {
        'fname': user.fname,
        'lname': user.lname,
        'email': user.email,
        'phone': user.phone,
    }
    return render(request, "webpages/show_profile.html", data)


def edit_profile(request):
    sesson_id = request.session.get('id')
    user = User.objects.get(id=sesson_id)
    data = {
        'fname': user.fname,
        'lname': user.lname,
        'email': user.email,
        'phone': user.phone,
    }

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        mail = request.POST['email']
        phone = request.POST['phone']

        sesson_id = request.session.get('id')
        id = User.objects.get(id=sesson_id)

        User.objects.filter(id=sesson_id).update(lname=lname, fname=fname, email=mail, phone=phone)
        return redirect('show_profile')
    else:
        print("edit profile main error")
    return render(request, "webpages/edit_profile.html", data)


def change_password(request):
    sesson_id = request.session.get('id')
    user = User.objects.get(id=sesson_id)
    data = {
        'fname': user.fname,
        'lname': user.lname,
    }

    if request.method == "POST":
        oldpas = request.POST['oldpassword']
        # newpas = request.POST['newpassword']
        pw = request.POST['newpassword']
        pwd = hashlib.md5(pw.encode())
        newpas = pwd.hexdigest()
        if User.objects.filter(password=oldpas):
            User.objects.filter(id=sesson_id).update(password=newpas)
            return redirect('index')
        else:
            print("pas doesn't match")
    else:
        print('pass')
    return render(request, "webpages/change_password.html", data)


# def forgot_password(request):
#     sesson_id = request.session.get('id')
#     user = User.objects.get(id=sesson_id)
#     data = {
#         'fname': user.fname,
#         'lname': user.lname,
#     }

#     email = request.POST['email']

#     # # -- Twilio OTP --
#     # client = Client('AC30576d420472c7d4202e072d68d75fee', '0d6151d4542dcbadc8cc1dd0f4808be5')

#     # message = client.messages \
#     #     .create(
#     #     body=f'Hello, {user.fname} Your OTP Is: 192329',
#     #     from_='+(440) 379-8608',
#     #     to='+919601964052'
#     # )
#     # print(message.sid)
#     return render(request, "webpages/forgot_password.html", data)

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        is_already_created = User.objects.filter(email=email)
        if is_already_created:
            otp = randint(100000, 999999)
            print("OTP IS")
            print(otp)
            subject = 'Otp verification'
            message = f"Your Is {otp}"
            from_email = 'footwear1153@gmail.com'
            to_email = [email]
            send_mail(subject, message, from_email, to_email)
            print("Configuration Mail Send")

            return render(request, 'webpages/otp.html', {'otp':otp, 'email':email})
        else:
            msg1 = "Email Is Not Registed"
            return render(request, 'webpages/forgot_password.html', {'email': email, 'msg':msg1})
    else:
        print("error")
        return render(request, 'webpages/forgot_password.html')
    
def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        cotp = request.POST['cotp']
        email = request.POST['email']
        print(email)
        if otp == cotp:
            return render(request, 'webpages/newpassword.html',{'email':email})
        else:
            msg = "Incorrect OTP"
            return render(request, 'webpages/otp.html', {'msg':msg, 'otp':otp})
    else:
        return render(request, 'webpages/otp.html')
    
def newpassword(request):
    if request.method == "POST":
        # password = request.POST['password']
        pw = request.POST['password']
        pwd = hashlib.md5(pw.encode())
        password = pwd.hexdigest()
        email = request.POST['email']
        user = User.objects.get(email=email)
        user.password = password
        user.save()
        msg1 = "Your Password Has Been Changed"
        return render(request, 'webpages/index.html', {'msg':msg1})
    else:
        return render(request, 'webpages/newpassword.html')


def about(request):
    return render(request, "webpages/about.html")


def contact(request):
    sessionId = request.session.get('id')
    user = User.objects.get(id=sessionId)
    if request.method == "POST":
        Subject = request.POST['subject']
        Message = request.POST['message']
        obj = Contacts(subject=Subject,message=Message,userid=user)
        print(obj.subject)
        obj.save()

    return render(request, "webpages/contact.html",{'user':user})


def men(request):
    return render(request, "webpages/men.html")


def women(request):
    return render(request, "webpages/women.html")

def review(request,id):
    if request.method == 'POST':
        sessionId = request.session.get('id')
        user = User.objects.get(id=sessionId) 
        prod = Product.objects.get(id=id)
        userReview = request.POST['title'] 
        userMsg = request.POST['review']
        if Reviews.objects.filter(userid=user.id, prodid=prod.id):
            print("You can't add reviews")
        else:          
            renew = Reviews(title=userReview, reviewMsg=userMsg, userid_id=user.id, prodid_id=prod.id, date=datetime.datetime.now())          
            renew.save()
        return redirect('index')
    return render(request, 'webpages/reviews.html')

def quickview(request,id):
    data = Product.objects.get(id=id)  
    rev = Reviews.objects.filter(prodid=data.id)    
    
    return render(request, "webpages/quickview.html",{'data':data,'rev':rev})

def add_to_wishlist(request):
    return render(request, "webpages/add-to-wishlist.html")

def address(request):
    sessionId = request.session.get('id')
    user = User.objects.get(id=sessionId) 
    useraddressid = Address.userId_id = user.id
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        postal = request.POST['postal']
        phone = request.POST['phone']
       
        addsave = Address(firstname=fname, lastname=lname, address1=address1, address2=address2, city=city, postalcode=postal, phoneno=phone, userId_id=useraddressid)
        addsave.save()
        return redirect('checkout')
        
    return render(request, 'webpages/address.html',{'user':user})

def editaddress(request,id):
    data = Address.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        postal = request.POST['postal']
        phone = request.POST['phone']

        objCheck = Address.objects.filter(id=id).update(firstname=fname, lastname=lname, address1=address1, address2=address2, city=city, postalcode=postal, phoneno=phone)
        return redirect('checkout')
    
    return render(request, 'webpages/editaddress.html',{'data':data})

def deladdress(request,id):
    data = Address.objects.get(id=id)
    data.delete()
    return redirect('checkout')

@csrf_exempt
def checkout(request):
    subtotal = 0
    shippingCharge = 60
    sessionId = request.session.get('id')
    user = User.objects.get(id=sessionId)
    addressid = Address.objects.filter(userId=user)

    cartProd = Cart.objects.filter(userid=user)
    for i in cartProd:
        subtotal = subtotal + i.price 
    subtotal += shippingCharge
     
    client = razorpay.Client(auth=('rzp_test_onjvGOsWSddoH1', '4vxijdpYeP67UIPEnNa9c0IR'))
    payment = client.order.create({'amount': subtotal * 100, 'currency': 'INR', 'payment_capture': '1', })

    return render(request, "webpages/checkout.html",{'addressid':addressid,'cartProd':cartProd,'user':user,'subtotal':subtotal,'client':client,'payment':payment})


def invoice(request, id):
    order_detail = Order.objects.get(id=id)
    print(order_detail.price)

    return render(request, 'webpages/invoice.html', {'order_detail': order_detail})


def buynow(request, id):
    sessionId = request.session.get('id')
    user = User.objects.get(id=sessionId)
    prod = Product.objects.get(id=id)
    addressid = Address.objects.filter(userId=user)
    total = int(prod.prodDisccountPrice) + 60
    print(total)

    client = razorpay.Client(auth=('rzp_test_onjvGOsWSddoH1', '4vxijdpYeP67UIPEnNa9c0IR'))
    payment = client.order.create({'amount': total * 100, 'currency': 'INR', 'payment_capture': '1', })
    request.session["pro_id"] = prod.id

    return render(request, "webpages/checkout.html",
                  {'addressid': addressid, 'user': user, 'prod': prod, 'subtotal': total, 'client': client,
                   'payment': payment})


def order_complete(request):
    return render(request, "webpages/order-complete.html")

@csrf_exempt
def payment_done(request):
    print(request.POST)

    return redirect('save_order')

def save_order(request):
    sessionId = request.session.get('id')
    user = User.objects.get(id=sessionId)
    address = Address.objects.get(id=3)
    print(address)
    varInvoice = randint(100000000, 999999999)
    order_id = uuid.uuid1()
    if 'pro_id' in request.session:
        prod = Product.objects.get(id=request.session['pro_id'])

        order = Order(name=prod.prodName, price=prod.prodDisccountPrice, quantity=prod.prodQuantity,
                      prodid=prod, userid=user,
                      image=prod.prod_img,
                      address=address, Invoice_No=varInvoice, orderid=order_id, Razorpay_order_id="",
                      Razorpay_payment_id="")
        order.save()

    else:
        # print("--------------------")
        # print(request.session.get('temp'))
        cart_obj_list = Cart.objects.filter(userid_id=user)

        for cart_obj in cart_obj_list:
            order = Order(name=cart_obj.name, price=cart_obj.price, quantity=cart_obj.quantity,
                          prodid=cart_obj.prodid, userid=cart_obj.userid,
                          image=cart_obj.image, Invoice_No=varInvoice, orderid=order_id, Razorpay_order_id="",
                          Razorpay_payment_id="")
            order.save()
            product_id_new = int(str(cart_obj.prodid).split('(')[1].replace(')', ''))
            print('prodid :', product_id_new)
            existsing_quantity = Product.objects.filter(id=product_id_new).values_list('prodQuantity')[0][0]
            print('existsing_quantity', existsing_quantity)
            new_quantity = int(existsing_quantity) - int(cart_obj.quantity)
            product = Product.objects.filter(id=product_id_new).update(prodQuantity=new_quantity)
            print('cart id :', cart_obj.id)
            remove_cart = Cart.objects.get(id=cart_obj.id)
            remove_cart.delete()

    return redirect("customer_order")


def view_order(request):
    return render(request, 'webpages/table_order.html')
    

def customer_order(request):
    sessionId = request.session.get('id')
    
    order_detail = Order.objects.filter(userid=sessionId)

    return render(request,'webpages/customer_order.html',{'order_detail':order_detail})


def product_detail(request):
    sessionId = request.session.get('id')
    order_detail = Order.objects.filter(userid=sessionId)
    return render(request, "webpages/product-detail.html",{'order_detail':order_detail})


def cartt(request):
    sid = request.session.get('id')
    uid = User.objects.get(id=sid)
    cartid = Cart.objects.filter(userid_id=uid)
    return render(request,'webpages/cartt.html',{'cartid':cartid})


def header(request):
    sid = request.session.get('id')
    uid = User.objects.get(id=sid)
    total = len(Cart.objects.filter(userid_id=uid))
    request.session['total'] = total
    return render(request, 'webpages/header.html',{'total':total})

# - - - - - - - Category pages - - - - - - - 

# - - - Men Category pages - - -

def men_loafer(request):
    product = Product.objects.filter(subcatid='1')
    
    return render(request, "cate_pages/Loafer.html",{'product':product})

def men_Chukkas(request):
    product = Product.objects.filter(subcatid='2')
    return render(request, "cate_pages/Chukkas.html",{'product':product})

def men_Oxfords(request):
    product = Product.objects.filter(subcatid='7')
    return render(request, "cate_pages/Oxfords.html",{'product':product})


# - - - Women Category pages - - -

def women_ConeHeels(request):
    product = Product.objects.filter(subcatid='3')
    return render(request, "cate_pages/ConeHeels.html",{'product':product})

def women_KittenHeels(request):
    product = Product.objects.filter(subcatid='4')
    return render(request, "cate_pages/KittenHeels.html",{'product':product})

def women_SlingbackHeels(request):
    product = Product.objects.filter(subcatid='8')
    return render(request, "cate_pages/SlingbackHeels.html",{'product':product})


# - - - Kids Category pages - - -

def kids_ToddlerShoe(request):
    product = Product.objects.filter(subcatid='7')
    return render(request, "cate_pages/ToddlerShoe.html",{'product':product})

def kids_SchoolShoes(request):
    product = Product.objects.filter(subcatid='6')
    return render(request, "cate_pages/SchoolShoes.html",{'product':product})

def kids_AthleticShoes(request):
    product = Product.objects.filter(subcatid='9')
    return render(request, "cate_pages/AthleticShoes.html",{'product':product})


def shoes(request,id): 
    data = Product.objects.get(id=id)
    return render(request, "cate_pages/shoes.html",{'data':data})



# def cartt_add(request):
#
#     product = request.POST.get('product')
#     cart = request.session.get('cart')
#     if cart:
#         quantity = cart.get(product)
#         if quantity:
#             cart[product] = quantity+1
#         else:
#             cart[product] = 1
#     else:
#         cart = {}
#         cart[product] = 1
#
#     request.session['cart'] = cart
#     print(request.session['cart'])
#     return redirect('index')


def cartt_add(request, id):
    #id = request.session.get("id")
    #user = User_register.objects.get(id=id)
    #print('customer id:',customer)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    print('product id:',id)
    cart.add(product=product)
    if request.POST:
        name = request.POST['name']
        image = request.POST['image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        prodid = request.POST['product']
        user_id = request.session['id']
        print('user_id :',user_id)
        print('quantity :',quantity,id)
        if int(quantity) < 1:
            messages.error(request,'product is not available')
        if Cart.objects.filter(prodid=id, userid=user_id).exists():
            existsing_quantity = Cart.objects.filter(prodid=id,userid=user_id).values_list('quantity')[0][0]
            print('existsing_quantity:',existsing_quantity)
            existsing_quantity += 1
            print('existsing_quantity +:', existsing_quantity)
            per_pro_price = product.prodPrice
            print('per_pro_price:', per_pro_price)
            total_amt = int(existsing_quantity) * int(per_pro_price)
            print('total_amt:', total_amt)
            cart = Cart.objects.filter(userid=user_id)                         
            Cart.objects.filter(prodid=id, userid=user_id).update(quantity=existsing_quantity,price=total_amt)
            return redirect('index')

        #request.session['cart'] = dict(id=id, quantity=quantity)
        obj = Cart(name=name,image=image,price=price,quantity=1)
        obj.prodid_id = prodid
        obj.userid_id = user_id
        obj.save()

    return redirect(reverse('cartt'),{'product':product})


def item_clear(request, id):
    cart = Cart.objects.get(id=id)
    print('Remove id:',id)
    cart.remove(cart)
    return redirect("checkout")


def item_increment(request, id):
    quantity = Cart.objects.filter(id=id).values_list('quantity')[0][0]
    print('quantity :',quantity)
    #cart = Cart.objects.get(id=id)
    product_id = Cart.objects.filter(id=id).values_list('prodid_id')[0][0]
    print('increment id:', id, product_id)
    per_pro_price = Product.objects.filter(id=product_id).values_list('prodPrice')[0][0]
    quantity += 1
    print('addition quantity:',int(quantity),int(per_pro_price))
    total_amt = int(quantity) * int(per_pro_price)
    print('total_amt :',total_amt)
    Cart.objects.filter(id=id).update(quantity=quantity,price=total_amt)

    return HttpResponseRedirect(reverse('cartt'))


def item_decrement(request, id):
    quantity = Cart.objects.filter(id=id).values_list('quantity')[0][0]
    print('quantity :', quantity)
    # cart = Cart.objects.get(id=id)
    product_id = Cart.objects.filter(id=id).values_list('prodid_id')[0][0]
    print('increment id:', id, product_id)
    per_pro_price = Product.objects.filter(id=product_id).values_list('prodPrice')[0][0]
    quantity -= 1
    print('addition quantity:', int(quantity), int(per_pro_price))
    total_amt = int(quantity) * int(per_pro_price)
    print('total_amt :', total_amt)
    Cart.objects.filter(id=id).update(quantity=quantity, price=total_amt)

    return HttpResponseRedirect(reverse('cartt'))


def cart_clear(request,id):
    cart = Cart.objects.get(id=id)
    print('id:', id)
    cart.delete()
    return redirect('cartt')

