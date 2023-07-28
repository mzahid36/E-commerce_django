from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    BannerImg,
    PaymentInfo
)

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'name', 'division','district','thana','villorroad','zipcode']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['id', 'title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','product','quantity','ordered_date','status']

@admin.register(BannerImg)
class BannerImgAdmin(admin.ModelAdmin):
    list_display = ['img_src']

@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ['img_src']

