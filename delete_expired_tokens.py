#!/usr/bin/env python3
import os
import dotenv

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graffiti_site.settings')
from django.core.management import execute_from_command_line

execute_from_command_line(['manage.py', 'delete_expired_tokens'])
