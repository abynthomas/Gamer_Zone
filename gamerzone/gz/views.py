from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import razorpay
import datetime
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.
def mainpage(request):
    return render(request, 'main_page.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forget.html')


def reset_password(request, token):
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
        else:
            messages.info(request, "Password doesn't match", extra_tags="signup")
    return render(request, 'reset.html',{'token':token})


def user_message(req):
    if req.method=='POST':
        nm=req.POST['name']
        email=req.POST['email']
        sub=req.POST['subject']
        msg=req.POST['message']
        send_mail(f'{sub} from user {req.user.email}', f'{msg}','settings.EMAIL_HOST_USER', [email], fail_silently=False)

    return render(req,'user_message.html')


def login(request):
    if request.method=='POST':
        a=request.POST['email']
        b=request.POST['password']
        try:
            data=User.objects.get(email=a)
            if data.password==b:
                request.session['user']=a
                return redirect(userhome)
            else:
                messages.error(request,'Password Incorrect')
        except Exception:
            if a=='admin@gmail.com' and b=='admin':
                request.session['admin']=a
                return redirect(adminhome)
                # messages.success(request,'Admin Login Success')
    return render(request,'login.html')

def logout(request):
    if 'user' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(mainpage)

def register(request):
    if request.method=='POST':
        a=request.POST.get('name')
        b=request.POST.get('phone')
        c=request.POST.get('email')
        d=request.POST.get('password')
        e = request.POST.get('cnfpassword')
        if d == e:
            if User.objects.filter(email=c).exists():
                messages.info(request, "Email already Registered", extra_tags="signup")
                return redirect(register)
            else:
                val = User.objects.create(name=a, email=c, phone=b, password=d)
                val.save()
                send_mail('Registration Successful', f'{a} Your Gamerzone Account Has Been Successfully Registered. \nTHANK YOU For Registering',
                          'settings.EMAIL_HOST_USER', [c], fail_silently=False)
                return redirect(login)
        else:
            messages.info(request,"Password doesn't match", extra_tags="signup")
            return redirect(register)

    return render(request, 'register.html')


# ------------------------------ADMIN HOME------------------------------
def adminhome(request):
    if 'admin' in request.session:
        a=Product.objects.all()
        print(a)
        for i in a:
            print(i.pk)
            if i.original_quantity < 10:
                send_mail('Please Check The Stock',
                          f'The stock of {i.product_name} is less than the limit.\nPlease Update the stock',
                          'settings.EMAIL_HOST_USER', ['gmrznadmn@gmail.com'], fail_silently=False)
        return render(request, 'admin_home.html')
    return redirect(login)


# ------------------------------ADMIN PRODUCTS------------------------------
def adminlaptop(request):
    if 'admin' in request.session:
        d= Product.objects.filter(categories='laptop')
        return render(request,'admin_laptop.html',{'data':d})
    return redirect(login)

def adminmonitor(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='monitor')
        return render(request,'admin_monitor.html',{'data':d})
    return redirect(login)

def admincpu(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='cpu')
        return render(request,'admin_cpu.html',{'data':d})
    return redirect(login)

def adminps(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='playstation')
        return render(request,'admin_ps.html',{'data':d})
    return redirect(login)

def adminxbox(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='xbox')
        return render(request,'admin_xbox.html',{'data':d})
    return redirect(login)

def adminswitch(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='nintendo')
        return render(request,'admin_switch.html',{'data':d})
    return redirect(login)

def adminaccessories(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='accessories')
        return render(request,'admin_accessories.html',{'data':d})
    return redirect(login)

def adminfurniture(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='furniture')
        return render(request,'admin_furniture.html',{'data':d})
    return redirect(login)

def admingames(request):
    if 'admin' in request.session:
        d = Product.objects.filter(categories='games')
        return render(request,'admin_games.html',{'data':d})
    return redirect(login)



# ------------------------------ADMIN ADD/UPDATE/DELETE------------------------------
def adminadd(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.POST['product_name']
            b = int(request.POST['price'])
            p = request.FILES['picture']
            c = request.POST['description']
            d = request.FILES.getlist('image')
            e = request.POST['categories']
            f = request.POST['details']
            g = int(request.POST['quantity'])
            h = request.POST['subcategories']
            v = request.FILES['videos']
            lis=[]
            for image in d:
                imgs = Images(image=image)
                imgs.save()
                lis.append(imgs)

            data = Product(product_name=a, price=b, description=c, picture=p, categories=e, details=f, original_quantity=g, sub_categories=h, video=v)
            data.save()
            for i in lis:
                data.images.add(i)
            return redirect(adminlaptop)
        return render(request,'admin_add.html')
    return redirect(login)

def adminupdate(request,d):
    if 'admin' in request.session:
        if request.method=='POST':
            a = request.POST['product_name']
            b = int(request.POST['price'])
            c = request.POST['description']
            f = request.POST['details']
            g = request.POST['quantity']

            Product.objects.filter(pk=d).update(product_name=a, price=b, description=c, details=f, original_quantity=g)
            return redirect(adminlaptop)
        data=Product.objects.filter(pk=d)
        return render(request,'admin_update.html',{'data':data})
    return redirect(login)

def productdelete(request,d):
    if 'admin' in request.session:
        data=Product.objects.get(pk=d)
        data.delete()
        messages.success(request,'Succefully Deleted')
        return redirect(adminlaptop)
    return redirect(login)

def adminproductview(request,d):
    if 'admin' in request.session:
        data=Product.objects.get(pk=d)
        return render(request,'admin_product_view.html',{'data':data,'d':d})
    return redirect(login)



# ------------------------------ADMIN USER DETAILS------------------------------
def adminuser(request):
    if 'admin' in request.session:
        order = Order.objects.filter(payment_status='PAID',product_status='Order Placed')
        order1 = Order.objects.filter(payment_status='PAID',product_status='Preparing')
        order2 = Order.objects.filter(payment_status='PAID',product_status='Packing')
        order3 = Order.objects.filter(payment_status='PAID',product_status='Ready For Delivery')
        order4 = Order.objects.filter(payment_status='PAID',product_status='Out For Delivery')
        return render(request,'admin_user.html',{'data':order,'data1':order1,'data2':order2,'data3':order3,'data4':order4})
    return redirect(login)




def adminviewusers(request):
    if 'admin' in request.session:
        d=User.objects.all()
        return render(request,'admin_view_users.html',{'data':d})
    return redirect(login)


def userdelete(request,d):
    data=User.objects.filter(email=d)
    data.delete()
    messages.success(request,'Succefully Deleted')
    return redirect(adminviewusers)

def adminrecentorders(request):
    if 'admin' in request.session:
        order = Order.objects.filter(product_status='Delivered').order_by('-purchase_date')
        return render(request,'admin_recent_orders.html',{'data': order})
    return redirect(login)


def adminorderupdate(request,d):
    if 'admin' in request.session:
        ord = Order.objects.get(pk=d)
        e = ord.user.email
        f = ord.product_order
        g = ord.name
        print(g)
        if request.method == 'POST':
            a = request.POST.get('odsts')
            b = request.POST.get('inst')
            Order.objects.filter(pk=d).update(product_status=a, instruction=b)

            send_mail(f'{a}',
                      f'Hey {g},\n\nYour {f} is {a},\n{b} \n\n THANK YOU.',
                      'settings.EMAIL_HOST_USER', [e], fail_silently=False)
            return redirect(adminuser)
        return render(request,'admin_order_update.html',{'data':ord})
    return redirect(login)

def adminusermail(request):
    if 'admin' in request.session:
        d = Mail.objects.all()
        return render(request,'admin_user_mail.html',{'data':d})
    return redirect(login)

def adminmessages(request):
    if 'admin' in request.session:
        d = Messages.objects.all()
        return render(request,'admin_messages.html',{'data':d})
    return redirect(login)





# ------------------------------USER------------------------------


# ------------------------------User Navbar------------------------------
def userhome(request):
    if 'user' in request.session:
        return render(request,'user_home.html')
    return redirect(login)

def myaccount(request):
    if 'user' in request.session:
        a = User.objects.get(email=request.session['user'])
        return render(request,'my_account.html',{'data':a})
    return redirect(login)

def updateprofile(request):
    if 'user' in request.session:
        if request.method == 'POST':
            a = request.POST.get('upname')
            b = request.POST.get('upphone')
            d = request.POST.get('upaddress')
            e = request.POST.get('upcity')
            h = request.POST.get('upstate')
            f = request.POST.get('upcountry')
            g = request.POST.get('upzipcode')
            User.objects.filter(email=request.session['user']).update(name=a, phone=b, address=d, city=e, country=f, zipcode=g, state=h)
            messages.success(request, 'Profile Updated')
            return redirect(myaccount)

def changepassword(request):
    if 'user' in request.session:
        if request.method == 'POST':
            a = request.POST.get('curpass')
            b = request.POST.get('newpass')
            c = request.POST.get('conpass')
            try:
                data = User.objects.get(email=request.session['user'])
                if data.password == a:
                    if b == c:
                        User.objects.filter(email=request.session['user']).update(password=b)
                        messages.success(request, 'Password Updated')
                        return redirect(myaccount)
                    else:
                        messages.error(request, 'Passwords Do not Match')
                        return redirect(myaccount)
                else:
                    messages.error(request, 'Password Incorrect')
                    return redirect(myaccount)
            except Exception:
                return redirect(myaccount)






def userrecentorders(request):
    if 'user' in request.session:
        user = User.objects.get(email=request.session['user'])
        order = Order.objects.filter(user=user,payment_status='PAID').order_by('-purchase_date')
        return render(request, 'user_recent_orders.html',{'data':order})
    return redirect(login)



# ------------------------------USER CART------------------------------
def addtocart(request,d):
    a = User.objects.get(email=request.session['user'])
    b = Product.objects.get(pk=d)
    data =Cart.objects.create(cart_user_details=a, cart_product_details=b)
    data.save()
    return redirect(viewcart)

def viewcart(request):
    if 'user' in request.session:
        user = User.objects.get(email=request.session['user'])
        cart_items = Cart.objects.filter(cart_user_details=user)
        qty = 0
        total = 0
        for i in cart_items:
            qty += i.cart_quantity
            total += i.cart_product_details.price * i.cart_quantity
        if not cart_items:
            return render(request, 'cart.html')

        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'qty': qty})
    return redirect(login)

def deletecart(request,d):
    data = Cart.objects.get(pk=d)
    data.delete()
    messages.success(request,'Succefully Deleted')
    return redirect(viewcart)


def increment_quantity(request, cart_id):
    cart_item = Cart.objects.get(pk=cart_id)
    if cart_item.cart_quantity >= 1:
        cart_item.cart_quantity += 1
        cart_item.save()
        cart_item.total_price=cart_item.cart_quantity * cart_item.cart_product_details.price
        cart_item.save()
    return redirect(viewcart)

def decrement_quantity(request, cart_id):
    cart_item = Cart.objects.get(pk=cart_id)
    if cart_item.cart_quantity > 1:
        cart_item.cart_quantity -= 1
        cart_item.save()
    return redirect(viewcart)


# ------------------------------User Wishlist------------------------------
def addtowishlist(request,d):
    a = User.objects.get(email=request.session['user'])
    b = Product.objects.get(pk=d)
    data =Wishlist.objects.create(wishlist_user_details=a, wishlist_product_details=b)
    data.save()
    return redirect(wishlist)

def wishlist(request):
    if 'user' in request.session:
        user = User.objects.get(email=request.session['user'])
        wishlist_items = Wishlist.objects.filter(wishlist_user_details=user)
        return render(request, 'wishlist.html',{'wishlist_items':wishlist_items})
    return redirect(login)

def deletewishlist(request,d):
    data = Wishlist.objects.get(pk=d)
    data.delete()
    messages.success(request,'Succefully Deleted')
    return redirect(wishlist)


# ------------------------------PAYMENT------------------------------
def checkout(request,d):
    user = User.objects.get(email=request.session['user'])
    pro = Product.objects.get(pk=d)

    if request.method=='POST':
        a = request.POST.get('chname')
        c = request.POST.get('chaddress')
        m = request.POST.get('chcity')
        e = request.POST.get('chstate')
        f = request.POST.get('chcountry')
        g = request.POST.get('chzipcode')
        h = request.POST.get('chphone')
        i = request.POST.get('chnotes')
        k = int(request.POST.get('chqty'))
        l = int(request.POST.get('chtotal'))
        val = Order.objects.create(user=user, name=a, address=c, city=m, state=e, country=f, zip_code=g, phone=h, notes=i, product_order=pro, quantity=k, total_price=l )
        val.save()
        request.session['order_name']= pro.product_name
        request.session['order_id'] = val.pk

        return redirect(payment,l,d,k)
    return render(request, 'checkout.html',{'data':pro, 'user':user})


def payment(request,l,d,k):
    pro = Product.objects.get(pk=d)
    amount = l * 100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    Product.objects.filter(pk=pro.id).update(original_quantity=pro.original_quantity-k)
    # status='PAID'
    # Order.objects.filter(pk=v).update(payment_status=status)
    return render(request, "payment.html",{'amount':amount})


def paymentsuccess(request):
    user = User.objects.get(email=request.session['user'])
    a = request.session['order_id']
    print(a)
    b = 'PAID'
    c = request.session['order_name']
    print(c)
    Order.objects.filter(pk=a).update(payment_status=b)
    send_mail('Payment Successful',
              f'Hey {user.name}, Your payment was successful and order for {c} has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
              'settings.EMAIL_HOST_USER', [user.email], fail_silently=False)
    send_mail('New Order',
              f' {user.name}, has placed a new order for {c}\nPlease review and update the order status',
              'settings.EMAIL_HOST_USER', ['gmrznadmn@gmail.com'], fail_silently=False)
    return render(request, "payment_success.html")





def checkoutcart(request,total,qty):
    user = User.objects.get(email=request.session['user'])
    pro=Cart.objects.filter(cart_user_details=user)
    order_ids = []
    if request.method == 'POST':
        a = request.POST.get('chname')
        c = request.POST.get('chaddress')
        d = request.POST.get('chcity')
        e = request.POST.get('chstate')
        f = request.POST.get('chcountry')
        g = request.POST.get('chzipcode')
        h = request.POST.get('chphone')
        l = int(request.POST.get('chtotal'))
        for i in pro:
            cn = i.cart_product_details
            cq = i.cart_quantity
            ct = i.cart_product_details.price * i.cart_quantity
            v=Order(user=user, name=a, address=c, city=d, state=e, country=f, zip_code=g, phone=h, notes=i, product_order=cn,quantity=cq,total_price=ct)
            v.save()
            value1 = v.pk
            order_ids.append(value1)
            Product.objects.filter(pk=i.cart_product_details.pk).update(original_quantity=i.cart_product_details.original_quantity-cq)
        request.session['order_ids'] = order_ids
        return redirect(paymentcart, l)

    return render(request,'checkout_cart.html',{'user':user,'data':pro,'total':total,'qty':qty})


def paymentcart(request,l):
    amount = l * 100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment_cart.html",{'amount':amount})


def paymentsuccess_cart(request):
    usr = User.objects.get(email=request.session['user'])
    order_ids = request.session.get('order_ids', [])
    for i in order_ids:
        c = i
        b = 'PAID'
        Order.objects.filter(pk=c).update(payment_status=b)
    send_mail('Payment Successful',
              f'Hey {usr.name}, Your payment was successful and your ordered items has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
              'settings.EMAIL_HOST_USER', [usr.email], fail_silently=False)
    send_mail('New Order',
              f' {usr.name}, has placed a some new orders\nPlease review and update the order status',
              'settings.EMAIL_HOST_USER', ['gmrznadmn@gmail.com'], fail_silently=False)
    return render(request, "payment_success.html")


# ------------------------------User Products------------------------------
def userlaptop(request):
    if 'user' in request.session:
        hp = Product.objects.filter(sub_categories='HP', categories='laptop')
        asus = Product.objects.filter(sub_categories='ASUS',categories='laptop')
        acer = Product.objects.filter(sub_categories='ACER',categories='laptop')
        lenovo = Product.objects.filter(sub_categories='LENOVO',categories='laptop')
        msi = Product.objects.filter(sub_categories='MSI',categories='laptop')
        return render(request,'user_laptop.html',{'hp':hp,'asus':asus,'acer':acer,'lenovo':lenovo,'msi':msi})
    return redirect(login)

def usermonitor(request):
    if 'user' in request.session:
        lg = Product.objects.filter(sub_categories='LG',categories='monitor')
        acer = Product.objects.filter(sub_categories='ACER',categories='monitor')
        msi = Product.objects.filter(sub_categories='MSI',categories='monitor')
        return render(request, 'user_monitor.html',{'lg':lg,'acer':acer,'msi':msi})
    return redirect(login)

def usercpu(request):
    if 'user' in request.session:
        d = Product.objects.filter(categories='cpu')
        return render(request, 'user_cpu.html',{'data':d})
    return redirect(login)

def userps(request):
    if 'user' in request.session:
        d = Product.objects.filter(categories='playstation')
        return render(request, 'user_ps.html',{'data':d})
    return redirect(login)

def userxbox(request):
    if 'user' in request.session:
        d = Product.objects.filter(categories='xbox')
        return render(request, 'user_xbox.html',{'data':d})
    return redirect(login)

def userswitch(request):
    if 'user' in request.session:
        d = Product.objects.filter(categories='nintendo')
        return render(request, 'user_switch.html',{'data':d})
    return redirect(login)

def useraccessories(request):
    if 'user' in request.session:
        mouse = Product.objects.filter(sub_categories='MOUSE',categories='accessories')
        keyboard = Product.objects.filter(sub_categories='KEYBOARD',categories='accessories')
        headphone = Product.objects.filter(sub_categories='HEADPHONES',categories='accessories')
        return render(request, 'user_accessories.html',{'mouse':mouse,'keyboard':keyboard,'headphone':headphone})
    return redirect(login)

def userfurniture(request):
    if 'user' in request.session:
        chair = Product.objects.filter(sub_categories='CHAIR',categories='furniture')
        table = Product.objects.filter(sub_categories='TABLE',categories='furniture')
        return render(request, 'user_furniture.html',{'chair':chair,'table':table})
    return redirect(login)

def usergames(request):
    if 'user' in request.session:
        xbox = Product.objects.filter(sub_categories='XBOX',categories='games')
        ps = Product.objects.filter(sub_categories='PLAYSTATION',categories='games')
        nintendo = Product.objects.filter(sub_categories='NINTENDO',categories='games')
        pc = Product.objects.filter(sub_categories='PC',categories='games')
        return render(request, 'user_games.html',{'xbox':xbox,'ps':ps,'nintendo':nintendo,'pc':pc})
    return redirect(login)



# ------------------------------User Product View------------------------------
def userproductview(request,d):
    if 'user' in request.session:
        data = Product.objects.get(pk=d)
        return render(request, 'user_product_view.html', {'data': data, 'd': d})
    return redirect(login)





# ------------------------------User Footer------------------------------
def mail(request):
    m = request.POST['mail']
    data =Mail.objects.create(mail=m)
    data.save()
    send_mail('Subscribed',
              f'Welcome to GAMERZONE\n Your email has been successfully registered for our newsletters\nWe will notify you about the latest products and updates\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
              'settings.EMAIL_HOST_USER', [m], fail_silently=False)
    return render(request,'user_home.html')


def aboutus(request):
    if 'user' in request.session:
        return render(request, 'about_us.html')
    return redirect(login)

def contactus(request):
    if 'user' in request.session:
        if request.method == 'POST':
            n = request.POST['mname']
            e = request.POST['memail']
            p = request.POST['mphone']
            m = request.POST['mmsg']
            data = Messages.objects.create(name=n,mail=e,number=p,message=m)
            data.save()
            send_mail('New Message',
                      f' {n}, send you a new message\n\n{m}\n\nContact info:\nEmail : {e}\nPhone number : {p}',
                      'settings.EMAIL_HOST_USER', ['gmrznadmn@gmail.com'], fail_silently=False)
        return render(request, 'contact_us.html')
    return redirect(login)

def privacypolicy(request):
    if 'user' in request.session:
        return render(request, 'privacy_policy.html')
    return redirect(login)

def termsconditions(request):
    if 'user' in request.session:
        return render(request, 'terms_conditions.html')
    return redirect(login)


# def search(request):
#     if 'user' in request.session:
#         if request.method=='POST':
#             a = request.POST.get('sc')
#             b = request.POST.get('sb')
#             data=Product.objects.filter(categories=a,sub_categories=b)
#             print(data)
#         return render(request, 'search.html',{'data':data})
#     return redirect(login)

def search(request):
    if 'user' in request.session:
        if request.method == 'POST':
            category = request.POST.get('sc')
            product_name = request.POST.get('sb')

            # If you want to filter based on both category and product name
            if category and product_name:
                data = Product.objects.filter(categories=category, sub_categories=product_name)
            # If you only want to filter based on category
            elif category:
                data = Product.objects.filter(categories=category)
            else:
                # Handle the case when no filters are applied
                data = Product.objects.all()

            return render(request, 'search.html', {'data': data})

    return redirect(login)











def blank(request):
    return render(request, 'blank.html')

def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

def store(request):
    return render(request, 'store.html')