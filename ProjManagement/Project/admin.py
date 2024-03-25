from django.contrib import admin
from .models import *
from Authentication.models import *

tables = [Status, Project, Task, User, Role, UserLogins, Team ]

admin.site.register(tables)