# sales/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.contrib.auth.models import User

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.user_id, u.username, a.password 
                    FROM Users u
                    JOIN Authentication a ON u.user_id = a.user_id
                    WHERE u.username = %s
                    """,
                    [username]
                )
                result = cursor.fetchone()
                
            if result:
                user_id, stored_username, stored_password = result
                if stored_password == password:  # Normally, you should hash the password
                    user, created = User.objects.get_or_create(username=stored_username, defaults={'id': user_id})
                    if created:
                        user.set_password(stored_password)  # Hash the password if needed
                        user.save()
                    return user
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None