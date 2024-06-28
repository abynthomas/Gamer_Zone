"""
URL configuration for gamerzone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gz import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.mainpage),
    path('login',views.login),
    path('logout',views.logout,name='logout'),
    path('register',views.register),

    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),





    path('admin_home',views.adminhome),
    path('admin_laptop',views.adminlaptop),
    path('admin_monitor',views.adminmonitor),
    path('admin_cpu',views.admincpu),
    path('admin_ps',views.adminps),
    path('admin_xbox',views.adminxbox),
    path('admin_switch',views.adminswitch),
    path('admin_accessories',views.adminaccessories),
    path('admin_furniture',views.adminfurniture),
    path('admin_games',views.admingames),

    path('admin_add_product',views.adminadd),
    path('admin_update/<int:d>',views.adminupdate),
    path('admin_product_view/<int:d>',views.adminproductview),
    path('product_delete/<int:d>',views.productdelete),

    path('admin_user',views.adminuser),
    path('admin_view_users',views.adminviewusers),
    path('user_delete/<d>',views.userdelete),
    path('admin_recent_orders',views.adminrecentorders),
    path('admin_order_update/<int:d>',views.adminorderupdate),
    path('admin_user_mail',views.adminusermail),
    path('admin_messages',views.adminmessages),



    path('user_home',views.userhome,name='userhome'),
    path('my_account',views.myaccount,name='my_account'),
    path('update_profile',views.updateprofile),
    path('change_password',views.changepassword),

    path('wishlist',views.wishlist,name='wishlist'),
    path('add_to_wishlist/<int:d>',views.addtowishlist),
    path('delete_wishlist/<int:d>',views.deletewishlist),

    path('add_to_cart/<int:d>',views.addtocart),
    path('cart',views.viewcart,name='cart'),
    path('delete_cart/<int:d>',views.deletecart),
    path('customer_cart/increment/<int:cart_id>/', views.increment_quantity, name='increment_quantity'),
    path('customer_cart/decrement/<int:cart_id>/', views.decrement_quantity, name='decrement_quantity'),

    path('checkout/<int:d>',views.checkout),
    path('checkout_cart/<int:total>/<int:qty>',views.checkoutcart),
    path('payment/<int:l>/<int:d>/<int:k>',views.payment),
    path('payment_cart/<int:l>',views.paymentcart),
    path('payment_success',views.paymentsuccess),
    path('payment_success_cart',views.paymentsuccess_cart),

    path('user_recent_orders',views.userrecentorders,name='user_recent_orders'),

    path('user_laptop',views.userlaptop,name='user_laptop'),
    path('user_monitor',views.usermonitor,name='user_monitor'),
    path('user_cpu',views.usercpu,name='user_cpu'),
    path('user_ps',views.userps,name='user_ps'),
    path('user_xbox',views.userxbox,name='user_xbox'),
    path('user_switch',views.userswitch,name='user_switch'),
    path('user_accessories',views.useraccessories,name='user_accessories'),
    path('user_furniture',views.userfurniture,name='user_furniture'),
    path('user_games',views.usergames,name='user_games'),

    path('user_product_view/<int:d>',views.userproductview),

    path('about_us',views.aboutus,name='about_us'),
    path('contact_us',views.contactus,name='contact_us'),
    path('privacy_policy',views.privacypolicy,name='privacy_policy'),
    path('terms_conditions',views.termsconditions,name='terms_conditions'),

    path('mail',views.mail),
    path('search',views.search),




    path('blank',views.blank),
    path('index',views.index),
    path('product',views.product),
    path('store',views.store),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
