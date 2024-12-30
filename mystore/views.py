from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Store, Customer, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from .forms import SignUpForm, PostingProducts, UpdateUserForm, ChangePasswordForm, UserInfoForm, CustomerInfoForm
from django.db.models import Q, Count
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
import json
from cart.cart import Cart
from geopy.distance import geodesic
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.db import transaction
from .utils import determine_delivery_system
from .forms import PostingProducts



def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


# class SubmitCartView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         # Provide pre-filled data if necessary
#         customer, _ = Customer.objects.get_or_create(user=request.user)
#         serializer = CustomerSerializer(customer)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         user = request.user
#         customer, _ = Customer.objects.get_or_create(user=user)
#         serializer = CustomerSerializer(customer, data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             store = Store.objects.first()
#             if not store:
#                 raise ValidationError("No store available.")

#             delivery_system = determine_delivery_system(serializer.validated_data['city'], store.city)
#             order = Order.objects.create(customer=customer, store=store, delivery_system=delivery_system)

#             return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
def submit_cart(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CustomerInfoForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            store = Store.objects.first()

            delivery_system = determine_delivery_system(customer.city, store.city)
            order = Order.objects.create(customer=customer, store=store, delivery_system=delivery_system)

            return redirect('payment_page', order_id=order.id)
    else:
        form = CustomerInfoForm(instance=customer)

    return render(request, 'submit_cart.html', {'form': form})


# class PaymentPageView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, order_id):
#         order = get_object_or_404(Order, id=order_id)
#         return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment.html', {'order': order})


from mystore.models import Product, Category
from mystore.serializers import ProductSerializer, CategorySerializer

# class SearchView(APIView):
#     def get(self, request):
#         query = request.GET.get('q', '').strip()
#         if not query:
#             return Response({'error': 'Query parameter is missing or empty'}, status=status.HTTP_400_BAD_REQUEST)

#         products = Product.objects.filter(name__icontains=query)
#         categories = Category.objects.filter(name__icontains=query)

#         product_data = ProductSerializer(products, many=True).data
#         category_data = CategorySerializer(categories, many=True).data

#         return Response({
#             'products': product_data,
#             'categories': category_data
#         }, status=status.HTTP_200_OK)



def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': 'Query parameter is missing or empty'}, status=400)

    products = Product.objects.filter(name__icontains=query)
    categories = Category.objects.filter(name__icontains=query)

    product_results = [
        {
            'id': product.id,
            'name': product.name,
            'image': product.image.url if product.image else '',
            'price': str(product.price),
            'url': reverse('product', args=[product.id]),
        }
        for product in products
    ]

    category_results = [
        {
            'id': category.id,
            'name': category.name,
            'url': reverse('category', args=[category.id]),
        }
        for category in categories
    ]

    return JsonResponse({
        'products': product_results,
        'categories': category_results,
    })



def homepage(request):
    billboards = [
        {'image_url': '/static/images/billboard1.png', 'alt_text': 'Best Offer 1'},
        {'image_url': '/static/images/billboard2.png', 'alt_text': 'Best Offer 2'},
        {'image_url': '/static/images/billboard3.png', 'alt_text': 'Best Offer 3'},
    ]
    
    categories_with_products = Category.objects.annotate(product_count=Count('product')).filter(product_count__gt=0)
    
    categories_data = []
    for category in categories_with_products:
        products = Product.objects.filter(category=category)[:10]
        categories_data.append({
            'category_name': category.name,
            'products': products,
        })
    
    return render(request, 'home.html', {
        'billboards': billboards,
        'categories_data': categories_data,
    })


def store_list(request):
    stores = Store.objects.filter(user__profile__is_approved=True)
    return render(request, 'store_list.html', {'stores':stores})


def store_profile(request, store_id):
    store = get_object_or_404(Store, id=store_id, is_approved=True)
    products = store.products.all()
    return render(request, 'store_page.html', {'store':store, 'products':products})


def store_map(request):
    stores = Store.objects.filter(
        user__profile__is_approved=True 
    )
    
    stores_data = []
    for store in stores:
        stores_data.append({
            'id': store.id,
            'store_name': store.store_name,
            'address': store.address,
            'latitude': store.latitude,
            'longitude': store.longitude,
            'store_profile_url': reverse('store_page', args=[store.id]),
            'store_kind': store.store_kind 
        })

    return render(request, 'store_map.html', {'stores_json': json.dumps(stores_data)})

def set_store_location(request):
    try:
        store = Store.objects.get(user=request.user)
    
    except Store.DoesNotExist:
        return HttpResponse("Store does not exist for this user", status=404)


    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            store.latitude = latitude
            store.longitude = longitude
            store.save()
        return redirect('register')
    

    context = {
        'initial_latitude': store.latitude if store else None,
        'initial_longitude': store.longitude if store else None,
        'store_name': store.store_name if store else 'Your Store' 
    }
    
    return render(request, 'store_location.html')



def get_nearby_stores(user_lat, user_lon, radius_km):
    stores = Store.objects.all()
    nearby_stores = []

    user_location = (user_lat, user_lon)

    for store in stores:
        store_location = (store.latitude, store.longitude)
        distance = geodesic(user_location, store_location).kilometers

        if distance <= radius_km:
            nearby_stores.append(store)

    return nearby_stores


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Info Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You must be logged in to access that page.")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',  {"categories":categories})


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect('update_user')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
                
        else:
            form = ChangePasswordForm(current_user, request.POST)
            return render(request, "update_password.html", {'form':form})
        
    else:
        messages.success(request, "You must be logges in to view that page")
        return render('home')


    return render(request, "update_password.html", {})

def update_user(request):

    user_form = UpdateUserForm(instance=request.user)
    
    latitude, longitude = None, None
    if hasattr(request.user, 'store'):
        latitude = request.user.store.latitude
        longitude = request.user.store.longitude
    elif hasattr(request.user, 'customer'):
        latitude = request.user.customer.latitude
        longitude = request.user.customer.longitude

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user = user_form.save()

            # Handling location update
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if latitude and longitude:
                if hasattr(request.user, 'store'):
                    store = request.user.store
                    store.latitude = latitude
                    store.longitude = longitude
                    store.save()
                elif hasattr(request.user, 'customer'):
                    customer = request.user.customer
                    customer.latitude = latitude
                    customer.longitude = longitude
                    customer.save()

            if hasattr(user, 'profile') and user.profile.role == 'store':
                store = Store.objects.get(user=user)
                if 'profile_picture' in user_form.cleaned_data and user_form.cleaned_data['profile_picture']:
                    store.profile_picture = user_form.cleaned_data['profile_picture']
                if 'billboard_picture' in user_form.cleaned_data and user_form.cleaned_data['billboard_picture']:
                    store.billboard_picture = user_form.cleaned_data['billboard_picture']
                store.save()

            return redirect('update_user')

    return render(request, 'update_user.html', {
        'user_form': user_form,
        'latitude': latitude,
        'longitude': longitude
    })


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',  {"categories":categories})



def category(request, pk):
    try:
        category = get_object_or_404(Category, pk=pk)
        sort_order = request.GET.get('sort', 'default')
        products = Product.objects.filter(category=category)


         # Applying sorting based on query parameter
        if sort_order == 'price_increasing':
            products = products.order_by('price')
        elif sort_order == 'price_decreasing':
            products = products.order_by('-price')
        else:
            products = products.order_by('id')


        return render(request, 'category.html', {
            'category': category,
            'products': products,
            'current_sort': sort_order
        })
        
    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist")
        return redirect('home')


def base_context(request):
    categories = Category.objects.all()
    return {'categories': categories}


def about(request):
    return render(request, 'about.html', {})


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_owner = product.store.user == request.user
    return render(request, 'product.html', {'product': product, 'is_owner': is_owner})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Only allow the store owner to edit
    if product.store.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this product.")

    if request.method == 'POST':
        form = PostingProducts(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', pk=product.pk)
    else:
        form = PostingProducts(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Checking ownership
    if product.store.user != request.user:
        return JsonResponse({'error': "You are not allowed to delete this product."}, status=403)

    if request.method == 'POST':
        product.delete()
        return JsonResponse({'success': True, 'redirect_url': reverse('store_page', args=[product.store.id])})

    return JsonResponse({'error': "Invalid request method."}, status=400)


def profile_under_review(request):
    return render(request, 'profile_under_review.html')


def store_page(request, store_id):
    # Getting the store
    store = Store.objects.get(id=store_id)
    
    products = Product.objects.filter(store=store)

    grouped_products = {}
    for product in products:
        category_name = product.category.name if product.category else "Uncategorized"
        if category_name not in grouped_products:
            grouped_products[category_name] = []
        grouped_products[category_name].append(product)

    return render(request, 'store_page.html', {
        'store': store,
        'grouped_products': grouped_products,
        'profile_picture': store.profile_picture,
        'billboard_picture': store.billboard_picture,
    })


@login_required
def posting_product(request):
    try:
        profile = Profile.objects.get(user=request.user)
        store = Store.objects.get(user=request.user)

        if profile.role != 'store' or not profile.is_approved:
            messages.error(request, "Only approved stores can post products.")
            return redirect('home')

    except (Profile.DoesNotExist, Store.DoesNotExist):
        messages.error(request, "Only stores can post products.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PostingProducts(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.store = store
            new_product.save()

            messages.success(request, "Product posted successfully!")
            return redirect('store_page', store_id=store.id)

        else:
            print("Form is invalid:")
            print(form.errors)
            messages.error(request, "Failed to post the product. Please check the form.")

    else:
        form = PostingProducts()

    return render(request, 'postingproduct.html', {'form': form})
   

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            store_name = form.cleaned_data['store_name']
            address = form.cleaned_data['address']
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            u = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            u.refresh_from_db()
            u.save()

            role = form.cleaned_data.get('role')
            p = Profile(user=u, role=role, phone=phone)
            p.save()

            if p.role == 'customer':
                c = Customer(user=u, email=email, phone=phone)
                c.latitude = latitude
                c.longitude = longitude
                c.address = address
                c.save()

            store_kind = form.cleaned_data.get('store_kind')
            if role == 'store':
                s = Store.objects.create(user=u)
                s.latitude = latitude
                s.longitude = longitude
                s.address = address
                s.store_name = store_name
                s.store_kind = store_kind
            

                # Saving profile picture and billboard picture if they exist
                if 'profile_picture' in request.FILES:
                    s.profile_picture = request.FILES['profile_picture']
                if 'billboard_picture' in request.FILES:
                    s.billboard_picture = request.FILES['billboard_picture']
                
                s.save()
            if role == 'store':
                return redirect('profile_under_review')
            else:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    print('Authentication failed.')
            return redirect('home')
    
    return render(request, 'register.html', {'form': form})

from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', block=True)
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            # Getting users saved cart from database
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.add(product=key, quantity=value)

                if user.profile.role == 'store':
                    return redirect('store_page', store_id=user.profile.id)
                
                else:
                    return redirect('home')

            messages.success(request, ("You have been logged in..."))
            return redirect('home')
        else:
            messages.success(request, ("There was a an error, please try again"))
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})
    

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                profile = Profile.objects.get(user=user)
                if profile.role == 'store' and not profile.is_approved:
                    messages.error(request, "Your profile is under review. Please wait for approval.")
                    return redirect('profile_under_review')
                else:
                    login(request, user)
                    return redirect('home')
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('home')

