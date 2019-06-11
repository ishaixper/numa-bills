from django.contrib import admin

# Register your models here.
from bills.models import Bill, Detection

admin.site.register(Bill)


class DetectionAdmin(admin.ModelAdmin):
    ordering = ["-created_on"]


admin.site.register(Detection, DetectionAdmin)
