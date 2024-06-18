from collections import defaultdict
import dis
from email import message
import json
import re
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.db.models import Count, Avg, Min, Max
from core.models import Coupon,Product,Category,Vendor,CartOrder, CartOrderItems,ProductImages,ProductReview,Wishlist,Address
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import razorpay
import calendar
from django.db.models.functions import ExtractMonth

from userauths.models import ContactUs, Profile
from django.core import serializers

from django.contrib.contenttypes.models import ContentType

# Create your views here.

def index(request):
    # product = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True)
    categories = Category.objects.all()

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0

    context = {
        "products":products,
        "categories":categories
    }
    return render(request, 'core/index.html', context)

def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0

    context = {
        "products":products
    }
    return render(request, 'core/shop.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    # Retrieve the content type of the product model
    product_content_type = ContentType.objects.get_for_model(Product)

    # Fetch the tags associated with the filtered products and annotate the product count
    tags = (
        Tag.objects.filter(taggit_taggeditem_items__content_type=product_content_type, taggit_taggeditem_items__object_id__in=products)
                .annotate(product_count=Count('taggit_taggeditem_items__object_id', distinct=True))
                .order_by('name')
    )

    min_max_price = products.aggregate(Min("price"), Max("price"))

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0

    context = {
        "products":products,
        "categories":category,
        "tags":tags,
        "min_max_price":min_max_price,
    }
    return render(request, 'core/category-product-list.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    # category = Category.objects.get(cid=cid)

    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)
    for p in related_products:
        product_review_stats = ProductReview.objects.filter(product=p).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        p.avg_rating = product_review_stats['avg_rating'] or 0
        p.review_count = product_review_stats['review_count'] or 0

    categories = Category.objects.all()

    p_images = product.p_images.all()

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False
    
    product_review_stats = ProductReview.objects.filter(product=product).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )

    product.avg_rating = product_review_stats['avg_rating'] or 0
    product.review_count = product_review_stats['review_count'] or 0

    context = {
        "product":product,
        "p_images":p_images,
        "related_products":related_products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form,
        "make_review":make_review,
        "categories":categories,
    }
    return render(request, 'core/product-detail.html', context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")


    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    
    # Extract unique categories for the matched products
    # Calculate product count for each category
    categories = defaultdict(int)
    for product in products:
        categories[product.category] += 1

    # Convert the defaultdict to a list of tuples
    categories = list(categories.items())

    min_max_price = products.aggregate(Min("price"), Max("price"))

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0

    context = {
        "products":products,
        "tags":tag,
        "categories":categories,
        "min_max_price":min_max_price,
    }

    return render(request, "core/tag.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user':user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews,
        }

    )

def search_view(request):
    query=request.GET.get('q')

    # products=Product.objects.filter(product_status="published", title__icontains=query, description__icontains=query).order_by("-date")
    
    # Filter the products based on our query
    products = Product.objects.filter(
        product_status="published",
        title__icontains=query,
        description__icontains=query
    ).order_by("-date")

    # Extract unique categories for the matched products
    # Calculate product count for each category
    categories = defaultdict(int)
    for product in products:
        categories[product.category] += 1

    # Convert the defaultdict to a list of tuples
    categories = list(categories.items())

    

    

    # Retrieve the content type of the product model
    product_content_type = ContentType.objects.get_for_model(Product)

    # Fetch the tags associated with the filtered products and annotate the product count
    tags = (
        Tag.objects.filter(taggit_taggeditem_items__content_type=product_content_type, taggit_taggeditem_items__object_id__in=products)
                .annotate(product_count=Count('taggit_taggeditem_items__object_id', distinct=True))
                .order_by('name')
    )

    min_max_price = products.aggregate(Min("price"), Max("price"))

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0


    context = {
        'products':products,
        'query':query,
        'categories':categories,
        'tags':tags,
        "min_max_price": min_max_price,
    }

    return render(request, "core/search.html", context)

def add_to_cart(request):
    cart_product = {}

    pid=request.GET['pid']
    price=float(Product.objects.get(pid=pid).price)
    image=str(Product.objects.get(pid=pid).image.url)

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': price,
        'image': image,
        'pid': request.GET['pid'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']: 
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    
    return JsonResponse({
        "data":request.session['cart_data_obj'], 
        "totalcartitems":len(request.session['cart_data_obj'])
        })

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = Product.objects.get(pid=item['pid']).price
            cart_total_amount += int(item['qty']) * float(price)
        
        totalcartitems= len(request.session['cart_data_obj'])

        if totalcartitems < 1:
            messages.warning(request, "Your cart is empty")
            return redirect("core:index")

        context = {
        "cart_data":request.session['cart_data_obj'], 
        "totalcartitems":len(request.session['cart_data_obj']),
        "cart_total_amount":cart_total_amount
        }

        return render(request, "core/cart.html", context)

        
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = Product.objects.get(pid=item['pid']).price
            cart_total_amount += int(item['qty']) * float(price)



        context = render_to_string("core/async/cart-list.html", {
        "cart_data":request.session['cart_data_obj'], 
        "totalcartitems":len(request.session['cart_data_obj']),
        "cart_total_amount":cart_total_amount
        })

    return JsonResponse({"data":context, "totalcartitems":len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = Product.objects.get(pid=item['pid']).price
            cart_total_amount += int(item['qty']) * float(price)



        context = render_to_string("core/async/cart-list.html", {
        "cart_data":request.session['cart_data_obj'], 
        "totalcartitems":len(request.session['cart_data_obj']),
        "cart_total_amount":cart_total_amount
        })

    return JsonResponse({"data":context, "totalcartitems":len(request.session['cart_data_obj'])})


@login_required
def checkout(request):
    try:
        oid=request.session['oid']
        order = CartOrder.objects.get(oid=oid)
        
    except KeyError:
        oid = CartOrder.objects.create(user=request.user).oid
        request.session['oid'] = oid
        order = CartOrder.objects.get(oid=oid)
        
    # Update order items based on the current state of the cart
    if 'cart_data_obj' in request.session:
        order_items = CartOrderItems.objects.filter(order=order)

        for o in order_items:
            if o.item not in request.session['cart_data_obj']:
                o.delete()
            
        for p_id, item in request.session['cart_data_obj'].items():
            product = get_object_or_404(Product, pid=item['pid'])
            price = product.price
            image = product.image.url
            pid=product.pid

            try:
                order_item = CartOrderItems.objects.get(order=order, item=item['title'])
                order_item.qty = item['qty']
                order_item.price = price
                order_item.total = int(item['qty']) * float(price)
                order_item.save()

            except CartOrderItems.DoesNotExist:
                order_item = CartOrderItems.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),
                    item=item['title'],
                    image=str(image),
                    qty=item['qty'],
                    price=float(price),
                    total=int(item['qty']) * float(price),
                    pid=str(pid)

                )
    
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
    order_items = CartOrderItems.objects.filter(order=order)

    if len(order_items) == 0:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")

    # Recalculate order total
    order_total = sum(item.total for item in order_items)
    order.price = order_total
    order.saved = 0
    order.total = order.price
    for coupon in order.coupons.all():
        discount = float(order.total) * (coupon.discount/100)
        order.total = float(order.total) - discount
        order.saved = float(order.saved) + discount
    order.save()

    if request.method == "POST":
        print("Request POST data:", request.POST)
        if 'apply-coupon' in request.POST:
            code = request.POST.get("code")
            coupon = Coupon.objects.filter(code=code, active=True).first()

            if coupon:
                if coupon in order.coupons.all():
                    messages.warning(request, "Coupon already activated")
                    return redirect("core:checkout")
                else:
                    discount = float(order.price) * (coupon.discount/100)
                    order.coupons.add(coupon)
                    # order.price = float(order.price) - discount
                    order.total = float(order.total) - discount
                    order.saved = float(order.saved) + discount

                    order.save()

                    messages.success(request, "Coupon activated")
                    return redirect("core:checkout")
            else:
                messages.error(request, "Coupon does not exist")
                return redirect("core:checkout")
            
        elif 'customer-details-checkout' in request.POST:
            
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            pincode = request.POST.get("pincode")

            print(pincode)

            if 'cart_data_obj' in request.session:
                print("e bi che")
                cart_total_amount = 0

                for p_id, item in request.session['cart_data_obj'].items():
                    price = Product.objects.get(pid=item['pid']).price
                    cart_total_amount += int(item['qty']) * float(price)

                order.price=cart_total_amount
                order.full_name=full_name
                order.phone=phone
                order.email=email
                order.address=address
                order.city=city
                order.state=state
                order.country=country
                order.pincode=pincode

                order.save()
                
                redirect_url = reverse('core:payment') + f'?oid={oid}'
                return redirect(redirect_url)


    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple addresses, only one should be activated.")
        active_address = None

    
                
    context = {
        "order":order,
        "order_items":order_items,
        # "cart_data":request.session['cart_data_obj'], 
        "totalcartitems":len(order_items),
        # "cart_total_amount":cart_total_amount,
        "active_address":active_address,
    }
           
    return render(request, "core/checkout.html", context)

def order_payment(request):
    oid=request.GET.get('oid')
    order = CartOrder.objects.get(oid=oid)

    if order.paid_status == "success":
        # Order has already been paid, redirect the user to another page or display a message
        messages.info(request, "Payment for this order has already been completed.")
        return redirect("core:checkout")

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment=client.order.create({
        'amount' : int(round(order.total,2)*100),
        'currency' : 'INR',
        'payment_capture' : 1,
    })

    order.razor_pay_order_id=payment['id']
    order.save()

    context = {
        "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "payment": payment,
    }
    return render(request, "core/payment.html", context)

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print(client.utility.verify_payment_signature(response_data))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = CartOrder.objects.get(razor_pay_order_id=provider_order_id)
        order.razor_pay_payment_id = payment_id
        order.razor_pay_payment_signature = signature_id
        order.save()
        
        if verify_signature(request.POST):
            order.paid_status = "success"
            order.cart_status = False
            request.session['cart_data_obj'] = {}
            del request.session['oid']
            order.save()
            return redirect("core:payment-completed", oid=provider_order_id)
        else:
            order.paid_status = "failure"
            order.save()
            return redirect('core:payment-failed', oid=provider_order_id)
    else:
        # payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        # provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
        #     "order_id"
        # )
        data = json.loads(request.body)

        payment_id = data.get("payment_id")
        provider_order_id = data.get("order_id")
        print(payment_id, provider_order_id)

        order = CartOrder.objects.get(razor_pay_order_id=provider_order_id)
        order.razor_pay_payment_id = payment_id
        order.paid_status = "failure"
        order.save()
        oid=order.oid
        return redirect('core:payment-failed', oid=provider_order_id)

@login_required
def payment_completed_view(request,oid):

    order = get_object_or_404(CartOrder, razor_pay_order_id=oid)

    # Check if the order's paid_status is "failure"
    if order.paid_status == "success":
        try:
            active_address = Address.objects.get(user=request.user, status=True)
        except:
            active_address = None

        orderitems = CartOrderItems.objects.filter(order=order)

        context = {
            "oid":oid,
            "data":orderitems, 
            "totalitems":len(orderitems),
            "total_amount":order.price,
            "active_address":active_address,
            "date":order.order_date,
        }
        
        # Render the payment completed page
        return render(request, 'core/payment-completed.html', context)
  
    else:
        # If the paid_status is not "success", redirect to another page
        return redirect('core:index')  # Redirect to the homepage or another page

'''
@login_required
def payment_completed_view(request,oid):
    order=CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    
    context = {
        "order":order,
    }
    
    return render(request, 'core/payment-completed.html', context)
'''

@login_required
def payment_failed_view(request,oid):

    order = get_object_or_404(CartOrder, razor_pay_order_id=oid)

    # Check if the order's paid_status is "failure"
    if order.paid_status == "failure":
        # Render the payment failed page
        return render(request, 'core/payment-failed.html', {'order': order})
    else:
        # If the paid_status is not "failure", redirect to another page
        return redirect('core:index')  # Redirect to the homepage or another page
            

def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user,cart_status=False, paid_status="success").order_by("-id")
    address = Address.objects.filter(user=request.user)
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    profile = Profile.objects.get(user=request.user)

    for o in orders:
        month.append(calendar.month_name[o['month']])
        total_orders.append(o["count"])

    if request.method == "POST":
        if 'add-address' in request.POST:
            address = request.POST.get("address")
            mobile = request.POST.get("mobile")

            new_address = Address.objects.create(
                user=request.user,
                address=address,
                mobile=mobile,
            )

            messages.success(request, "Address Added Successfully")
            return redirect("core:dashboard")
        
        elif 'update-profile' in request.POST:
                full_name = request.POST.get("full_name")
                phone = request.POST.get("phone")

                # Retrieve the Profile instance associated with the current user
                profile = request.user.profile
                
                # Update the fields
                profile.full_name = full_name
                profile.phone = phone
                
                # Save the changes
                profile.save()
                
                messages.success(request, "Profile updated successfully!")
                return redirect("core:dashboard")


    context = {
        "orders_list": orders_list,
        "address":address,
        "orders":orders,
        "month":month,
        "total_orders":total_orders,
        "profile":profile,
    }
    return render(request, "core/dashboard.html", context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
        
    context ={
        "order_items" : order_items,
    }
    return render(request, "core/order-detail.html", context)

    
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})



# Other Pages
def contact(request):
    if request.method == 'POST':
        full_name = request.POST['full_name'] 
        email = request.POST['email'] 
        phone = request.POST['phone'] 
        subject = request.POST['subject'] 
        message = request.POST['message']

        ContactUs.objects.create(full_name=full_name, email=email, phone=phone, subject=subject, message=message)
        
        messages.success(request, "Message send successfully!")
        return redirect("core:contact")

    return render (request, "core/contact.html")

def about_us(request): 
    return render (request, "core/about-us.html")

def privacy_policy(request): 
    return render(request, "core/privacy-policy.html")


@login_required
def wishlist_view(request):

    wishlist = Wishlist.objects.all()

    
    
    context = {
        "wishlist": wishlist
    }

    return render(request, "core/wishlist.html", context)

def add_to_wishlist(request):
    product_id=request.GET['id']
    product=Product.objects.get(id=product_id)

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool" : False
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )

        context ={
            "bool": True
        }

    return JsonResponse(context)

def remove_from_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    wishlist_product = Wishlist.objects.get(id=pid)
    delete_product = wishlist_product.delete()

    wishlist_json = serializers.serialize('json', wishlist)

    context = {
        "bool" : True,
        "wishlist": wishlist
    }

    data = render_to_string("core/async/wishlist-list.html", context)

    return JsonResponse({"data": data, "wishlist": wishlist_json})

# def filter_product(request):
#     categories = request.GET.getlist('category[]')
#     print(categories)
#     # tags = request.GET.getlist('tags[]')

#     min_price=request.GET.get('min_price')
#     max_price=request.GET.get('max_price')

#     products = Product.objects.filter(product_status="published").order_by("-id").distinct()
#     products = products.filter(price__gte=min_price)
#     products = products.filter(price__lte=max_price)

#     if len(categories) > 0:
#         products = products.filter(category__id__in=categories).distinct() # same as category.id.in

#     context = {
#         "products": products
#     }
#     data = render_to_string("core/async/product-list.html", context)

#     return JsonResponse({"data":data})



def filter_product(request):

    choice = {'1':'id', '3':'-date', '4':'price', '5':'-price'}

    categories_str = request.GET.get('category')
    categories = []

    if categories_str:
        categories = [int(cat_id) for cat_id in categories_str.split(',')]

    tags_str = request.GET.get('tag')
    tags = []

    if tags_str:
        tags = [t for t in tags_str.split(',')]

    sorting = request.GET.get('sorting')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    products = Product.objects.filter(product_status="published") #.order_by(choice[sorting])

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if len(categories)>0:
        products = products.filter(category__id__in=categories)

    if len(tags)>0:
        products = products.filter(tags__slug__in=tags)
    
    if search:
        products=products.filter(title__icontains=search, description__icontains=search).order_by("-date")


    products = products.distinct()

    # Calculate the average rating for each product
    for product in products:
        avg_rating = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']
        product.avg_rating = avg_rating or 0  # Set default to 0 if no reviews

    if sorting == '2':  # Sort by average rating
        products = sorted(products, key=lambda x: x.avg_rating or 0, reverse=True)
    else:  # Sort by other options
        products = products.order_by(choice.get(sorting), '-date')

    for product in products:
        product_review_stats = ProductReview.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        product.avg_rating = product_review_stats['avg_rating'] or 0
        product.review_count = product_review_stats['review_count'] or 0

    context = {
        "products": products
    }
    data = render_to_string("core/async/product-list.html", context)

    return JsonResponse({"data": data, "count":len(products)})

def footer(request):
    return render(request, 'core/footer.html')

def base(request):
    return render(request, 'base.html')
