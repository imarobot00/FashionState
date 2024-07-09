
# sales/management/commands/initialize_db.py
from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help='Initialize the Database with Custom SQL'

    def handle(self, *args, **kwargs):
        with open('sales/sql/create_table.sql', 'r') as f:
            sql=f.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)
        

        self.stdout.write(self.style.SUCCESS('Database initialized successfully.'))