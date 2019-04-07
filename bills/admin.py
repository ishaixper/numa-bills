from django.contrib import admin

# Register your models here.
from bills.models import Bill

admin.site.register(Bill)
