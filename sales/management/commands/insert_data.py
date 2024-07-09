
from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection

#Subclassing the BaseCommand
class Command(BaseCommand):
    help='Insert data into the database with Custom SQL'

    def handle(self, *args, **kwargs):
        with open('sales/sql/insert_data.sql','r') as f:
            sql = f.read()
        
        with connection.cursor() as cursor:
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
        self.stdout.write(self.style.SUCCESS('Data inserted successfully.'))
        

