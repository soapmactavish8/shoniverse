from re import subn
from unicodedata import category
from django.shortcuts import render, HttpResponse, redirect
from ast import Return
from django.shortcuts import render
from mysqlx import Session

from .models import *
from app1.models import *
from django.contrib import messages
from .render_report import  RenderReport
# Create your views here.
from django.views.generic import View


def admin_index(request):
    session_Id = request.session.get('adminSession')
    adminGet = admin.objects.get(adminEmail=session_Id)
    admindata = {
        'adminname':adminGet.adminEmail
    }

    return render(request, 'adminpage/admin_index.html',admindata)



# ----- Category Department -----

def add_category(request):
    if request.method == 'POST':
        catname = request.POST['catname']
        print(catname)
        obj  =  Category(c_name = catname)

        obj.save()

    return render(request, 'adminpage/add_category.html')

def manage_category(request):
    all = Category.objects.all()
    return render(request, 'adminpage/manage_category.html',{'all':all})

def edit_category(request,id):
    up_cat = Category.objects.get(id=id)
    data = {
        'c_name': up_cat.c_name
    }

    if request.method == 'POST':
        name = request.POST['catname']
        Category.objects.filter(id=id).update(c_name=name)
        return redirect('manage_category')
    else:
        pass
    return render(request, 'adminpage/edit_category.html',data)

def delete_category(request,id):
    del_cat = Category.objects.get(id=id)
    del_cat.delete()
    return redirect('manage_category')



# ----- Sub-Category Department -----

def add_subCategory(request):
    cat = Category.objects.all()
    if request.method == 'POST':
        s_name = request.POST['s_name']
        cat_name = request.POST['cat_name']
        obj = SubCategory(s_name=s_name)

        obj.catid_id = cat_name
        obj.save()
    return render(request, 'adminpage/add_sub_Category.html',{'cat':cat})


def manage_subCategory(request):
    all = SubCategory.objects.all()
    return render(request, 'adminpage/manage_sub_Category.html',{'all':all})
  

def edit_subcategory(request,id):
    all = SubCategory.objects.get(id=id)
    if request.method == "POST":
        subname = request.POST['subname']
        obj = SubCategory.objects.filter(id=id).update(s_name=subname)
        return redirect('manage_subCategory')
    return render(request, 'adminpage/edit_subcategory.html',{'all':all})


def delete_subcategory(request,id):
    del_sub = SubCategory.objects.get(id=id)
    del_sub.delete()
    return redirect('manage_subCategory')


# ----- Product Department -----

def add_product(request):
    cat = Category.objects.all()
    sub = SubCategory.objects.all()

    if request.method == 'POST':
        catid = request.POST['catid']
        subcatid = request.POST['subcatid']
        prodName = request.POST['prodName']
        prodDescription = request.POST['prodDescription']
        prodDescription1 = request.POST['prodDescription1']
        prodSize = request.POST['prodSize']
        prodColor = request.POST['prodColor']
        prodDisccountPrice = request.POST['prodDisccountPrice']
        prod_img = request.FILES['prod_img']
        stock = request.POST['stock']
        prodPrice = request.POST['prodPrice']
        prodQuantity = request.POST['prodQuantity']
        brand = request.POST['brand']

        obj = Product(prodName=prodName, prodDescription=prodDescription,prodDescription1=prodDescription1,prodSize=prodSize,prodColor=prodColor,prodDisccountPrice=prodDisccountPrice, prod_img=prod_img, stock=stock, prodPrice=prodPrice, prodQuantity=prodQuantity, brand=brand)
        obj.catid_id = catid
        obj.subcatid_id = subcatid
        obj.save()
   
    return render(request, 'adminpage/add_product.html',{'cat':cat,'sub':sub})

def manage_product(request):
    all = Product.objects.all()
    return render(request, 'adminpage/manage_product.html',{"all":all})

def manage_order(request):
    all = Order.objects.all()
    return render(request, 'adminpage/manage_order.html',{'all':all})

def manage_review(request):
    all = Reviews.objects.all()
    return render(request, 'adminpage/manage_review.html',{'all':all})

def manage_contect(request):
    all = Contacts.objects.all()
    return render(request, 'adminpage/manage_contect.html',{'all':all})


def edit_product(request,id):
    cat = Category.objects.all()
    sub = SubCategory.objects.all()
    prod = Product.objects.get(id=id)

    if request.method == 'POST':
        prodName = request.POST['prodName']
        prodDescription = request.POST['prodDescription']
        prodDescription1 = request.POST['prodDescription1']
        prodSize = request.POST['prodSize']
        prodColor = request.POST['prodColor']
        prodDisccountPrice = request.POST['prodDisccountPrice']
        prod_img = request.FILES['prod_img']
        stock = request.POST['stock']
        prodPrice = request.POST['prodPrice']
        prodQuantity = request.POST['prodQuantity']
        catid = request.POST['catname']
        subcatid = request.POST['subname']
        brand = request.POST['brand']
        if Product.objects.filter(prodName = prodName).exists():
            messages.error(request,"saas")
        else:
            form = Product.objects.filter(id=id).update(prodName=prodName,
                                                        prodDescription=prodDescription,
                                                        prodDescription1=prodDescription1,
                                                        prodSize=prodSize,
                                                        prodColor=prodColor,
                                                        prodDisccountPrice=prodDisccountPrice,
                                                        prod_img=prod_img,
                                                        stock=stock,
                                                        prodPrice=prodPrice,
                                                        prodQuantity=prodQuantity,
                                                        catid=catid,
                                                        subcatid=subcatid,
                                                        brand=brand)
            return redirect('manage_product')
    return render(request, 'adminpage/edit_product.html',{'cat':cat,'sub':sub,'prod':prod})


def delete_product(request,id):
    del_sub = Product.objects.get(id=id)
    del_sub.delete()
    return redirect('manage_product')

def change_order_status(request,id):
    order_detail = Order.objects.get(id=id)
    if order_detail.status == "Pending":
        order_detail.status = "Completed"
    else:
        order_detail.status = "Pending"     
    order_detail.save()
    return redirect('order_report')

def admin_login(request):
    if request.POST:
        adminName = request.POST["email"]
        adminPass = request.POST["password"]

        logCheck = admin.objects.filter(adminEmail=adminName, adminpass=adminPass)
        if logCheck:
            request.session['adminSession'] = adminName
            return redirect('admin_index')
        else:
            print("something went wrong in logcheck")
    else:
        print("Error on post")
    return render(request, 'adminpage/adminLogin.html')


def admin_logout(request):
    del request.session['adminSession']
    return redirect('index')

def user_report(request):
    user = User.objects.all()
    return render(request, 'adminpage/user_report.html', {'user': user})

def order_report(request):
    user = Order.objects.all()
    return render(request,'adminpage/order_report.html',{'user':user})

def order_detail(request,id):
    orderdetail = Order.objects.get(id=id)
    return render(request,'adminpage/order_detail.html',{'orderdetail':orderdetail})

class Pdf(View):

    def get(self, request):
        user = User.objects.all()
        today = timezone.now()
        params = {
            'today': today,
            'user': user,
            'request': request
        }
        return RenderReport.render_report('adminpage/pdf.html', params)

class PdfOrder(View):

    def get(self, request):
        user = Order.objects.all()
        today = timezone.now()
        params = {
            'today': today,
            'user': user,
            'request': request
        }
        return RenderReport.render_report('adminpage/order_pdf.html', params)
