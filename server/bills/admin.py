from django.contrib import admin

# Register your models here.
from bills.models import Bill, Detection

admin.site.register(Bill)
admin.site.register(Detection)