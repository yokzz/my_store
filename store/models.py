from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In review"),
    ("published", "Published"),
)

RATING = (
    (1, "★✩✩✩✩"),
    (2, "★★✩✩✩"),
    (3, "★★★✩✩"),
    (4, "★★★★✩"),
    (5, "★★★★★"),
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=63, default="toys")
    image = models.ImageField(upload_to="category", default="category.jpg")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Tags(models.Model):
    pass
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="ven", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=63, default="Madarima")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover_vendor.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="I am a Cool Vendor")
    
    address = models.CharField(max_length=127, null=True)
    city = models.CharField(max_length=63, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=63, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=63, default="100")
    shipping_on_time = models.CharField(max_length=63, default="100")
    authentic_rating = models.CharField(max_length=63, default="100")
    days_return = models.CharField(max_length=63, default="100")
    warranty_period = models.CharField(max_length=63, default="100")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    date_of_join = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prd", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=63, default ="Volleyball")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="products")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default="2.99")
    
    specifications = RichTextUploadingField(null=True, blank=True)
    type = models.CharField(max_length=63, default ="Organic", null=True, blank=True)
    stock_count = models.CharField(max_length=63, default="12", null=True, blank=True)
    life = models.CharField(max_length=63, default="365 Days", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Products"
    
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
        


####### Cart, Order, OrderItems and Address ######
        
        
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    email = models.EmailField()
    phone_number = models.CharField(max_length=63)
    
    address = models.CharField(max_length=127, null=True)
    country = models.CharField(max_length=127, blank=True, null=True)
    city = models.CharField(max_length=127, blank=True, null=True)
    state = models.CharField(max_length=127, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    saved = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    coupons = models.ManyToManyField("store.Coupon", blank=True)
    
    shipping_method = models.CharField(max_length=127, blank=True, null=True)
    tracking_id = models.CharField(max_length=127, blank=True, null=True)
    tracking_website = models.CharField(max_length=127, blank=True, null=True)
    
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    oid = ShortUUIDField(unique=True, length=2, max_length=30, alphabet="1234567890") 
    order_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    
    stripe_payment_intent = models.CharField(max_length=1000, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Card Order"
        
    
    

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    
    invoice_number = models.CharField(max_length=127)
    product_status = models.CharField(max_length=127)
    item = models.CharField(max_length=127)
    image = models.CharField(max_length=127)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=12, decimal_places=2, default="1.99")
    
    class Meta:
        verbose_name_plural = "Card Order Items"
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
    
######## Produts Review, wishlists, Address #######


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = RichTextUploadingField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
    
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlists"
    
    
    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=127, null=True)
    phone_number = models.CharField(max_length=127, null=True)
    country = models.CharField(max_length=63, blank=True, null=True)
    city = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Address"
        
    
class Coupon(models.Model):
    code = models.CharField(max_length=63)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    uses = models.IntegerField()
    use_count = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.code