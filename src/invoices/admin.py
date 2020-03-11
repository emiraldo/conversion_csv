from django.contrib import admin
from .models import UploadedFile, Invoice, InvoiceDetail
# Register your models here.

class InvoiceDetailInline(admin.StackedInline):
    model = InvoiceDetail
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = 'number', 'customer_name', 'customer_last_name', 'customer_identification'
    list_display_links = list_display
    inlines = InvoiceDetailInline,
