from ast import Add
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,Wishlist,Address
from django.contrib import messages
from django.db.models import Min, Max

from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag

def default(request):
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    try:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    except:
        wishlist_count = 0
        messages.warning(request, "You need to login before accessing your wishlist")
        

    categories = Category.objects.all()

    try:
        address=Address.objects.get(user=request.user)
    except:
        address=None

    
   
   
    product_content_type = ContentType.objects.get_for_model(Product)
    # tags = Tag.objects.filter(taggit_taggeditem_items__content_type=product_content_type).distinct()

    from django.db.models import Count

    tags = (
        Tag.objects.filter(taggit_taggeditem_items__content_type=product_content_type)
                .annotate(product_count=Count('taggit_taggeditem_items__object_id', distinct=True))
                .order_by('name')
    )


    # tags = Tag.objects.all()
 
    return {
        'categories':categories,
        'address':address,
        'wishlist_count': wishlist_count,
        'min_max_price':min_max_price,
        'tags':tags
    }