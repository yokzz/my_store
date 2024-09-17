from django.contrib import admin
from store.models import Product, Category, Vendor, CartOrder, CartOrderItems, Wishlist, Tags, ProductImages, ProductReview, Address, Coupon

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'pid', 'product_status']
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']
    
    
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'order_status', 'oid']
    

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'item', 'image', 'quantity', 'price', 'total']
    

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']
    

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    
    
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['user', 'address', 'status']
    
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "active"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
