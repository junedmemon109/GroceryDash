from django.contrib import admin
from core.models import Coupon, Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,Wishlist,Address
from userauths.models import User
# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'featured', 'product_status','pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

# class VendorAdmin(admin.ModelAdmin):
#     list_display = ['title', 'vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'mobile', 'status']
    list_display = ['user', 'address', 'mobile', 'status']

class CouponAdmin(admin.ModelAdmin):
    list_editable = ['discount', 'active']
    list_display = ['code', 'discount', 'active']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
