from django.urls import path, include
from core.views import about_us, add_to_wishlist, base, callback, cart_view, add_to_cart, ajax_add_review, category_list_view, category_product_list_view, checkout, contact, customer_dashboard, delete_item_from_cart, filter_product, footer, index, make_address_default, order_detail, order_payment, payment_completed_view, payment_failed_view, privacy_policy, product_detail_view, product_list_view, remove_from_wishlist, tag_list, search_view, update_cart, wishlist_view

app_name = 'core'

urlpatterns = [
    #Homepage
    path('', index, name='index'),
    path('products/', product_list_view, name='product_list'),
    path('product/<pid>/', product_detail_view, name='product_detail'),
    
    #Category
    path('category/', category_list_view, name='category_list'),
    path('category/<cid>/', category_product_list_view, name='category_product_list'),
    
    #Tags
    path('products/tag/<slug:tag_slug>/', tag_list, name="tags"),

    #Add Review
    path("ajax-add-review/<int:pid>", ajax_add_review, name="ajax-add-review"),

    # Search
    path("search/", search_view, name="search"),

    # Add to cart url
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    # Cart page url
    path("cart/", cart_view, name="cart"),

    # Delete item from cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    # Update cart
    path("update-cart/", update_cart, name="update-cart"),

    # # checkout URL
    # path("checkout/", checkout_view, name="checkout"),

    # # checkout URL
    # path("checkout/<oid>", checkout, name="checkout"),

    # checkout URL
    path("checkout/", checkout, name="checkout"),

    # path("save_checkout_info/", save_checkout_info, name="save_checkout_info"),

    

    # Dashboard URL
    path("dashboard/", customer_dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),

    # Making addresses default
    path("make-default-address/", make_address_default, name="make-default-address"),

    #PayPal URL
    path('paypal/', include('paypal.standard.ipn.urls')),

    # # Payment Successfull
    # path("payment-completed/", payment_completed_view, name="payment-completed"),

    # Payment Successfull
    path("payment-completed/<oid>/", payment_completed_view, name="payment-completed"),

    # Payment Failed
    path("payment-failed/<oid>/", payment_failed_view, name="payment-failed"),

    path("contact/", contact, name="contact"),

    path("payment/", order_payment, name="payment"),
    path("razorpay/callback/", callback, name="callback"),

    #wishlist
    path('wishlist/', wishlist_view, name="wishlist"),

    #ading to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    #Removing from wishlist
    path("remove-from-wishlist/", remove_from_wishlist, name="remove-wishlist"),

    path("filter-products/", filter_product, name="filter-product"),

    path("footer/", footer),
    path('privacy-policy', privacy_policy, name="privacy-policy"),
    path('about-us', about_us, name="about-us"),
    path('base', base),

]   