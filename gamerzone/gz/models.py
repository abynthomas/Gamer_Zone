from django.db import models

# ------------------------------Users------------------------------
class User(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=15, null=True)
    state = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=15, null=True)
    zipcode = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


# ------------------------------Product Images------------------------------
class Images(models.Model):
    image=models.ImageField()


# ------------------------------Products------------------------------
class Product(models.Model):
    sub_categories = models.CharField(max_length=20,null=True)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    picture = models.FileField()
    details = models.TextField()
    categories = models.CharField(max_length=20)
    images=models.ManyToManyField(Images,null=True)
    original_quantity = models.IntegerField()
    video = models.FileField(null=True)

    def __str__(self):
        return self.product_name


# ------------------------------Subscribed Mails------------------------------
class Mail(models.Model):
    mail = models.CharField(max_length=25)
    def __str__(self):
        return self.mail


# ------------------------------User to Admin Messages------------------------------
class Messages(models.Model):
    name = models.CharField(max_length=25)
    mail = models.CharField(max_length=25)
    number = models.CharField(max_length=15)
    message = models.TextField()
    def __str__(self):
        return self.name

# ------------------------------User Cart------------------------------

class Cart(models.Model):
    cart_product_details = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_user_details = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)


    def __str__(self) -> str:
        return f'{self.cart_user_details}'

# ------------------------------User Wishlist------------------------------

class Wishlist(models.Model):
    wishlist_product_details = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist_user_details = models.ForeignKey(User,on_delete=models.CASCADE)
    wishlist_quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.wishlist_user_details}'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    country = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=15)
    notes = models.CharField(max_length=50)
    product_order = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    payment_status = models.CharField(max_length=20,null=True)
    purchase_date = models.DateTimeField(auto_now=True, null=True)
    product_status = models.CharField(max_length=50,null=True, default='Order Placed')
    instruction = models.CharField(max_length=50,null=True, default='Your Order Has Been Successfully Placed')


    def __str__(self) -> str:
        return f'{self.name}'



class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)