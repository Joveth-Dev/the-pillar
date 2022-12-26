from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Populates the database with college and degree_programs'

    def handle(self, *args, **options):
        print('Populating university tables...')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        sql = Path(file_path).read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)
