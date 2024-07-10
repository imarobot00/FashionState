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
            items = get_items()
            new_items = get_new_items()
            return render(request, "Home/homepage.html", {
                'items': items,
                'new_items': new_items
            })
        else:
            return HttpResponse('Invalid username or password.')
    else:
        return HttpResponse('Invalid request.')

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
        cursor.execute("SELECT item_id, name, price, image_path FROM items")
        products = cursor.fetchall()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'Home/products.html', context)

@login_required
def product_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from items where item_id = %s", [id])
        product = cursor.fetchone()
    
    if not product:
        raise Http404("Product does not exist")
    
    product_dict = {
        'id': product[0],
        'name': product[1],
        'price': product[4],
        'description': product[8],
        'image': product[5]
    }
    return render(request, 'Home/sproduct.html', {'product': product_dict})
