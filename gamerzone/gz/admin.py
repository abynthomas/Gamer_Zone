from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Mail)
admin.site.register(Messages)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(PasswordReset)