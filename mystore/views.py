from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Store, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from .forms import SignUpForm, PostingProducts, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from geopy.distance import geodesic
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.db import transaction
# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import Point
# from .models import Store


@login_required
def store_map(request):
    stores = Store.objects.exclude(latitude__isnull=True, longitude__isnull=True)
    return render(request, 'store_map.html', {'stores':stores})


@login_required
def set_store_location(request):
    if request.method == "GET":
        return render(request, 'store_location.html')
    elif request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

    try:
        store = Store.objects.get(user=request.user)
        store.latitude = latitude
        store.longitude = longitude
        store.save()
        return redirect('update_user')
    except store.DoesNotExist:
        return HttpResponse("Store does not exist for this user", status=404)



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



def search(request):
    # Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query The Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "That Product Does Not Exist...")
            return render(request, "search.html", {})
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})

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
        # Did they fill out the form

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
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
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access that page.")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',  {"categories":categories})



def category(request, foo):
    # Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
        
    except:
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')



def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


@login_required
def store_page(request):
    if request.user.profile.role != 'store':
        return HttpResponseForbidden("You do not have access to this page.")
    
    # Logic for the store's page
    return render(request, 'store_page.html')


@login_required
def posting_product(request):

    try:
        if request.user.profile.role != 'store':
            return HttpResponseForbidden("You don't have permission to post products!")
    except Profile.DoesNotExist:
        return redirect('home')
    

    if request.method == 'POST':
        form = PostingProducts(request.POST, request.FILES)
        if form.is_valid():
            # image_object = form.instance()
            store = Store.objects.get(user=request.user)
            new_product = form.save(commit=False)
            new_product.store = store
            new_product.save()

            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            # category = form.cleaned_data.get('category')
            image = form.cleaned_data.get('image')
            price = form.cleaned_data.get('price')
            new_product = Product.objects.create(
                name=name,
                price=price,
                image=image,
                description=description
            )
            print("Product is created")
            new_product.refresh_from_db()
            print("Refreshed from db")
            new_product.save()
            print("Product saved")
            # messages.success(request, ("You have submitted a product successfuly"))
            return redirect('store_page')
        
        
        else:
            print("Unsuccessful saving...")
            messages.success(request, ("Ooops! Missed filling out the whole form..."))
            return redirect('posting-product')
        
    else:
        print("Unsuccessful saving 2...")
        form = PostingProducts()
    # return render(request, 'postingproduct.html', {'form':form, 'img_obj':image_object})
    return render(request, 'postingproduct.html', {'form':form})
    

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
    # Do all these steps to register the user
        # form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            u = User.objects.create_user(
                username = username,
                password = password,
                email=email,
            )
            u.refresh_from_db()
            u.save()

            role = form.cleaned_data.get('role')
            p = Profile(user=u, role=role, phone=phone)
            p.save()

            if p.role == 'customer':
                c = Customer(user=u, email=email, phone=phone)
                c.save()

            if p.role == 'store':
                s = Store(user=u)
                s.save()
            

            # log in user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed.')
        else:   
            messages.success(request, ("Whoops!!!"))
            return redirect('register')
    else:
        # Just show them the page
        return render(request, 'register.html', {'form':form})
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string t
            # o python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                cart = Cart(request)
                # Load through the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.add(product=key, quantity=value)

                if user.profile.role == 'store':
                    return redirect('store_page', store_id=user.profile.id)
                
                else:
                    return redirect('home')

            messages.success(request, ("You have been logged in..."))
            return redirect('home')
            # else:
            # return redirect('store_page')
        else:
            messages.success(request, ("There was a an error, please try again"))
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})

    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('home')

