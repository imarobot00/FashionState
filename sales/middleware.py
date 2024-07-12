# sales/middleware.py
from django.shortcuts import redirect
from django.db import connection

class RetailerLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.path == '/retailer_login/' and request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Authenticate retailer
            retailer = self.authenticate_retailer(email, password)
            if retailer:
                request.session['retailer_id'] = retailer['retailer_id']
                return redirect('retailer_dashboard')
            else:
                return redirect('retailer_login')  # Redirect back to login on failure

    def authenticate_retailer(self, email, password):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT r.retailer_id, r.email, ra.password 
                    FROM retailer r
                    JOIN retailer_authentication ra ON r.retailer_id = ra.retailer_id
                    WHERE r.email = %s
                    """,
                    [email]
                )
                result = cursor.fetchone()
                
            if result:
                retailer_id, stored_email, stored_password = result
                if stored_password == password:  # Normally, you should hash the password
                    return {'retailer_id': retailer_id, 'email': stored_email}
        except Exception as e:
            return None
        return None
