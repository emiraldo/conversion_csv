from django.contrib import admin
from .models import UploadedFile
# Register your models here.


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = 'pk', 'file', 'separator', 'token'
    list_display_links = list_display
