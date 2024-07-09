
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection,transaction
from django.core.paginator import Paginator
# Create your views here.
def index(request, name):
    return HttpResponse(f"This is a Fashion Retail Website.{name}")

from django.db import connection
#from django.http import HttpResponse


def start(request):
    return render(request, "Home/index.html")

def submit_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Use raw SQL to retrieve data by joining Users and Auth tables
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.username, a.password 
                FROM Users u
                JOIN Authentication a ON u.user_id = a.user_id
                WHERE u.username = %s
                """,
                [username]
            )
            result = cursor.fetchone()

        if result:
            stored_username, stored_password = result
            if stored_password == password:
                # Fetch items
                items = get_items()
                new_items= get_new_items()
                return render(request,"Home/homepage.html", {
                    'items': items,
                    'new_items':new_items
                    })
            else:
                return HttpResponse('Invalid password.')
        else:
            return HttpResponse('Username not found.')
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
                    # Insert into Users table
                    cursor.execute(
                        "INSERT INTO Users (username, email, phone_no) VALUES (%s, %s, %s);",
                        [username, email, phone_no]
                    )
                    # Retrieve the user_id of the newly inserted user
                    cursor.execute(
                        "SELECT user_id FROM Users WHERE username = %s;",
                        [username]
                    )
                    user_id = cursor.fetchone()[0]

                    # Insert into Auth table
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
        items=cursor.fetchall()
    
    return items


def shop(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT item_id, name, price, image_path FROM items")
        products = cursor.fetchall()

    paginator = Paginator(products, 12)  # Show 12 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Home/products.html', context)

def sproducts(request):
    return render(request, 'Home/sproducts.html')