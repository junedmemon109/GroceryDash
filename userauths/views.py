from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.models import CartOrder, CartOrderItems, Product
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from django.contrib.auth.hashers import check_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# User = settings.AUTH_USER_MODEL

# Create your views here.

def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, Your account was created successfully')
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1']
                                    )
            
            login(request, new_user)
            return redirect('core:index')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.GET.get('next')  # Retrieve the 'next' parameter from the URL
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                from django.db.models import Q

                unprocessed_orders = CartOrder.objects.filter(Q(user=request.user) &
                    Q(cart_status=True) &
                    (Q(paid_status="pending") | Q(paid_status="failure"))
                ).order_by('-order_date')

                if unprocessed_orders.exists():

                    # Get the most recent unprocessed order
                    recent_order = unprocessed_orders.first()
                    order_items = CartOrderItems.objects.filter(order=recent_order)

                    request.session['oid'] = str(recent_order.oid)
                    request.session['cart_data_obj'] = {}

                    # Initialize session with data from the recent order
                    for o in order_items:
                        try:
                            product = Product.objects.get(title=o.item)
                            request.session['cart_data_obj'][str(product.id)] = {
                                'title': str(o.item),
                                'qty': int(o.qty),
                                'price': float(o.price),
                                'image': str(o.image),
                                'pid': str(product.pid),
                            }
                        except Product.DoesNotExist:
                            # Handle the case where the product referenced by an order item doesn't exist
                            # You can log the error, ignore the item, or take appropriate action based on your application's logic
                            pass

                messages.success(request, 'You are logged in.')

                if next_url:
                    return redirect(next_url)  # Redirect to the original page
                else:
                    return redirect('core:index')
            else:
                messages.warning(request, 'Invalid email or password.')

        except User.DoesNotExist:
            messages.warning(request, f'User with email {email} does not exist.')

    
    return render(request, 'userauths/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You Logged Out.')

    return redirect('userauths:sign-in')

def profile_update(request):
    pass

@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if confirm_new_password != new_password:
            messages.error(request, 'Password does not match!')
            return redirect('userauths:change-password')
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('userauths:change-password')
        else:
            messages.error(request, 'Old password is incorrect!')
            return redirect('userauths:change-password')
    
    return render(request, 'userauths/change-password.html')
        