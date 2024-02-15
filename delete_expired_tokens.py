#!/usr/bin/env python3
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graffiti_site_api.prod_settings')
from django.core.management import execute_from_command_line

execute_from_command_line(['manage.py', 'delete_expired_tokens'])
