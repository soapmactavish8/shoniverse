from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from app1 import views 
from django.conf import settings
from django.conf.urls.static import static
from adminservices import views as adminsvs
from adminservices.views import Pdf, PdfOrder

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('add_to_wishlist', views.add_to_wishlist, name='add_to_wishlist'),
    path('checkout', views.checkout, name='checkout'),
    path('order_complete', views.order_complete, name='order-complete'),
    path('product_detail', views.product_detail, name='product-detail'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login, name='login'),
    path('quickview/<int:id>', views.quickview, name='quickview'),
    path('cartt', views.cartt, name='cartt'),
    path('cartt/add/<int:id>/', views.cartt_add, name='cartt_add'),
    path('cartt/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cartt/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cartt/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cartt/cart_clear/<int:id>', views.cart_clear, name='cart_clear'),
    path('show_profile',views.show_profile, name='show_profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),
    path('forgot_password',views.forgot_password, name='forgot_password'),
    path('otp ',views.otp, name='otp'),
    path('newpassword', views.newpassword, name="newpassword"),
    path('user_logout', views.user_logout, name='user_logout'),
    path('shoes/<int:id>', views.shoes, name='shoes'),
    path('invoice/<int:id>', views.invoice, name='invoice'),
    path('address', views.address, name='address'),
    path('editaddress/<int:id>', views.editaddress, name='editaddress'),
    path('deladdress/<int:id>',views.deladdress, name='deladdress'),
    path('header',views.header, name='header'),
    path('customer_order',views.customer_order, name='customer_order'),
    path('payment_done',views.payment_done, name='payment_done'),
    path('save_order',views.save_order, name='save_order'),
    path('view_order',views.view_order, name='view_order'),
    path('buynow/<int:id>',views.buynow, name='buynow'),
    path('review/<int:id>',views.review, name='review'),
   


# productpages urls
    path('men', views.men, name='men'),
    path('women', views.women, name='women'),


# Admin Services urls
    path('admin_index', adminsvs.admin_index, name='admin_index'),
    path('admin_logout', adminsvs.admin_logout, name='admin_logout'),
    path('add_category',adminsvs.add_category, name='add_category'),
    path('manage_category',adminsvs.manage_category, name='manage_category'),
    path('add_subCategory',adminsvs.add_subCategory, name='add_subCategory'),
    path('manage_subCategory',adminsvs.manage_subCategory, name='manage_subCategory'),
    path('add_product', adminsvs.add_product, name='add_product'),
    path('manage_product', adminsvs.manage_product, name='manage_product'),
    path('manage_order', adminsvs.manage_order, name='manage_order'),
    path('manage_review', adminsvs.manage_review, name='manage_review'),
    path('manage_contect', adminsvs.manage_contect, name='manage_contect'),

    path('order_detail/<int:id>',adminsvs.order_detail, name='order_detail'),
    

# Admin Crud_Operations
    path('admin_login', adminsvs.admin_login, name='admin_login'),

    path('edit_category/<int:id>', adminsvs.edit_category, name='edit_category'),
    path('delete_category/<int:id>', adminsvs.delete_category, name='delete_category'),

    path('edit_subcategory/<int:id>', adminsvs.edit_subcategory, name='edit_subcategory'),
    path('delete_subcategory/<int:id>', adminsvs.delete_subcategory, name='delete_subcategory'),

    path('edit_product/<int:id>', adminsvs.edit_product, name='edit_product'),
    path('delete_product/<int:id>', adminsvs.delete_product, name='delete_product'),
    path('change_order_status/<int:id>', adminsvs.change_order_status, name='change_order_status'),

    path('user_report', adminsvs.user_report, name='user_report'),
    path('render/pdf/', Pdf.as_view()),
    path('order_report',adminsvs.order_report,name='order_report'),
    path('render/orderpdf/', PdfOrder.as_view()),


# Category Page URLS
          # - - -  Men  - - - 
    path('men_loafer', views.men_loafer, name='men_loafer'),
    path('men_Chukkas', views.men_Chukkas, name='men_Chukkas'),
    path('men_Oxfords', views.men_Oxfords, name='men_Oxfords'),

          # - - -  Women  - - - 
    path('women_ConeHeels', views.women_ConeHeels, name='women_ConeHeels'),
    path('women_KittenHeels', views.women_KittenHeels, name='women_KittenHeels'),
    path('women_SlingbackHeels', views.women_SlingbackHeels, name='women_SlingbackHeels'),

          # - - -  Kids  - - - 
    path('kids_ToddlerShoe', views.kids_ToddlerShoe, name='kids_ToddlerShoe'),
    path('kids_SchoolShoes', views.kids_SchoolShoes, name='kids_SchoolShoes'),
    path('kids_AthleticShoes', views.kids_AthleticShoes, name='kids_AthleticShoes'),

    path('cartt_add',views.cartt_add,name='cartt_add'),
    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
