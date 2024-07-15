# sales/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.core.paginator import Paginator
from django.http import Http404

def index(request, name):
    return HttpResponse(f"This is a Fashion Retail Website.{name}")

def start(request):
    return render(request, "Home/index.html")

def submit_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to the homepage view
        else:
            return HttpResponse('Invalid username or password.')
    else:
        return HttpResponse('Invalid request.')

@login_required
def homepage(request):
    items = get_items()
    new_items = get_new_items()
    return render(request, "Home/homepage.html", {
        'items': items,
        'new_items': new_items
    })

def signup(request):
    return HttpResponse('Signup Window.')

def submit_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone_no = request.POST['phone_no']

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Users (username, email, phone_no) VALUES (%s, %s, %s);",
                        [username, email, phone_no]
                    )
                    cursor.execute(
                        "SELECT user_id FROM Users WHERE username = %s;",
                        [username]
                    )
                    user_id = cursor.fetchone()[0]

                    cursor.execute(
                        "INSERT INTO Authentication (user_id, password) VALUES (%s, %s);",
                        [user_id, password]
                    )
            return HttpResponse('Signed Up successfully')
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}')
    else:
        return HttpResponse('Invalid request.')

def get_items():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM items;")
        items = cursor.fetchall()
    return items

def get_new_items():
    with connection.cursor() as cursor:
        cursor.execute("select * from items order by created_at desc;")
        items = cursor.fetchall()
    return items

@login_required
def shop(request):
    with connection.cursor() as cursor:
        cursor.execute("select items.item_id,items.name,items.price,items.image_path,retailer.name from items join retailer on items.retailer_id=retailer.retailer_id;")
        products = cursor.fetchall()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'Home/products.html', context)

@login_required
@login_required
def product_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from items where item_id = %s", [id])
        product = cursor.fetchone()
        
        cursor.execute("SELECT * from items limit 4;")  # Fetch all items for the featured products section
        items = cursor.fetchall()
    
    if not product:
        raise Http404("Product does not exist")
    
    product_dict = {
        'id': product[0],
        'name': product[1],
        'price': product[4],
        'description': product[8],
        'image': product[5]
    }
    
    items_dict = [
        {
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'price': item[4],
            'image': item[5],
        }
        for item in items
    ]
    
    return render(request, 'Home/sproduct.html', {
        'product': product_dict,
        'items': items_dict,
    })

def retailer_login(request):
    return render(request, 'Home/retailer_login.html')

def retailer_dashboard(request):
    if 'retailer_id' not in request.session:
        return redirect('retailer_login')

    retailer_id = request.session['retailer_id']
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM items WHERE retailer_id = %s", [retailer_id])
        items = cursor.fetchall()

    return render(request, 'Home/retailer_dashboard.html', {'items': items})

@login_required
def cart(request):
    return render(request,'Home/cart.html')

@login_required
def profile(request):
    return render(request,'Home/profile.html')