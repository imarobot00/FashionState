# sales/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.core.paginator import Paginator
from django.http import Http404
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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

def retailer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        business_liscense_no = request.POST['business_liscense_no']
        address = request.POST['address']

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO retailer (name, address, business_license_no, phone_no, email) VALUES (%s, %s, %s, %s, %s);",
                        [username, address, business_liscense_no, phone_no, email]
                    )
                    cursor.execute(
                        "SELECT retailer_id FROM retailer WHERE name = %s;",
                        [username]
                    )
                    retailer_id = cursor.fetchone()[0]

                    cursor.execute(
                        "INSERT INTO retailer_authentication (retailer_id, password) VALUES (%s, %s);",
                        [retailer_id, password]
                    )
            return HttpResponse('Signed Up successfully')
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}')
    else:
        return HttpResponse('Invalid request.')

def retailer_dashboard(request):
    if 'retailer_id' not in request.session:
        return redirect('retailer_login')

    retailer_id = request.session['retailer_id']
    
    with connection.cursor() as cursor:
        # Get retailer details
        cursor.execute("SELECT name, email, phone_no FROM retailer WHERE retailer_id = %s", [retailer_id])
        retailer = cursor.fetchone()

        if retailer is None:
            return HttpResponse('Retailer not found.', status=404)

        retailer_details = {
            'name': retailer[0],
            'email': retailer[1],
            'phone_no': retailer[2],
        }
        
        # Get retailer's items
        cursor.execute("SELECT name, price, product_details, image_path FROM items WHERE retailer_id = %s", [retailer_id])
        items = cursor.fetchall()
        
        items_list = [{
            'name': item[0],
            'price': item[1],
            'description': item[2],
            'image_path': item[3],
        } for item in items]

    return render(request, 'Home/retailer_dashboard.html', {'retailer': retailer_details, 'items': items_list})



def submit_retailer(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['description']
        stocks = request.POST['stocks']
        image = request.FILES['image']
        retailer_id = request.session['retailer_id']

        # Define the uploads path within MEDIA_ROOT
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        # Ensure the uploads directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Save the image to the uploads directory
        image_name = image.name
        image_path = os.path.join(upload_dir, image_name)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Use the relative path for the database with forward slashes
        relative_image_path = os.path.join('uploads', image_name).replace('\\', '/')
        
        # Manually add the prefix '/'
        full_image_path = f'/media/{relative_image_path}'

        # Save the product details to the database
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO items (name, price, product_details, stocks, image_path, retailer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    [product_name, price, description, stocks, full_image_path, retailer_id]
                )

        return redirect('retailer_dashboard')

    return HttpResponse('Invalid request.')



@login_required
def cart(request):
    user_id = request.user.id  # Get the user ID of the logged-in user

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT product_id, product_name, price, image_path FROM cart WHERE user_id = %s', [user_id]
        )
        cart_items = cursor.fetchall()

    # Calculate the total price
    total_price = sum(item[2] for item in cart_items)

    return render(request, 'Home/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def profile(request):
    user_id = request.user.id

    # Step 1: Fetch user details and purchased item IDs
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT users.username, users.email, users.phone_no, purchase.item_id '
            'FROM purchase '
            'JOIN users ON purchase.user_id = users.user_id '
            'WHERE users.user_id = %s',
            [user_id]
        )
        user_details = cursor.fetchall()

    if not user_details:
        logger.info('No purchase details found for user_id: %s', user_id)
        combined_details = {
            'user_info': {
                'username': request.user.username,
                'email': request.user.email,
                'phone_no': ''  # Assuming phone_no is optional and may not be available
            },
            'items': []
        }
        return render(request, 'Home/profile.html', {'combined_details': combined_details})

    # Step 2: Extract item IDs from the user_details
    item_ids = [item[3] for item in user_details]

    # Step 3: Fetch detailed information for each item
    item_details = []
    if item_ids:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT item_id, name, price, product_details, image_path '
                'FROM items '
                'WHERE item_id IN %s',
                [tuple(item_ids)]
            )
            item_details = cursor.fetchall()

    # Combine user details with item details
    combined_details = {
        'user_info': {
            'username': user_details[0][0],
            'email': user_details[0][1],
            'phone_no': user_details[0][2]
        },
        'items': item_details
    }

    logger.info('Combined details for user_id %s: %s', user_id, combined_details)

    return render(request, 'Home/profile.html', {
        'combined_details': combined_details
    })

@login_required
def add_to_cart(request, item_id, name, price, image):
    user_id = request.user.id  # Get the user ID of the logged-in user

    try:
        with connection.cursor() as cursor:
            # Insert the item into the cart
            cursor.execute(
                'INSERT INTO cart (product_id, product_name, user_id, price, image_path) VALUES (%s, %s, %s, %s, %s)',
                [item_id, name, user_id, price, image]
            )

        return redirect('cart')  # Redirect to the cart view
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)

@csrf_exempt
@login_required
def checkout(request):
    if request.method == 'POST':
        user_id = request.user.id
        bank_account = request.POST.get('bank_account')
        total_price = request.POST.get('total_price')

        with connection.cursor() as cursor:
            # Fetch cart items for the user
            cursor.execute(
                "SELECT cart.product_id, items.retailer_id "
                "FROM cart "
                "JOIN items ON cart.product_id = items.item_id "
                "WHERE cart.user_id = %s",
                [user_id]
            )
            cart_items = cursor.fetchall()

            # Insert each purchase into the purchase table
            for cart_item in cart_items:
                product_id = cart_item[0]
                retailer_id = cart_item[1]

                cursor.execute(
                    "INSERT INTO purchase (user_id, item_id, retailer_id, bank_account, total_price, created_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    [user_id, product_id, retailer_id, bank_account, total_price, datetime.now()]
                )
                # Update the stock for each item
                cursor.execute(
                    "UPDATE items SET stocks = stocks - 1 WHERE item_id = %s",
                    [product_id]
                )

            # Clear the cart for the user
            cursor.execute("DELETE FROM cart WHERE user_id = %s", [user_id])

        return redirect('profile')

    return JsonResponse({'success': False})
