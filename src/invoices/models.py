from django.db import models

# Create your models here.


class UploadedFile(models.Model):

    file = models.FileField(upload_to='uploaded_files/')
    separator = models.CharField(max_length=10, verbose_name='separador')
    token = models.UUIDField()


class Invoice(models.Model):

    number = models.PositiveIntegerField(verbose_name='número de factura', unique=True)
    customer_name = models.CharField(max_length=255, verbose_name='nombres del cliente')
    customer_last_name = models.CharField(max_length=255, verbose_name='apellidos del cliente')
    customer_identification = models.CharField(max_length=100, verbose_name='identificación del cliente')


    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'


class InvoiceDetail(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_code = models.CharField(max_length=544, verbose_name='código del item')
    item_description = models.TextField(verbose_name='descripción del item')
    item_quantity = models.PositiveIntegerField(verbose_name='cantidad del item')
    unit_price = models.DecimalField(verbose_name='precio unitario', decimal_places=2, max_digits=10)
    total_price = models.DecimalField(verbose_name='precio total', decimal_places=2, max_digits=10)
    discount_rate = models.DecimalField(verbose_name='porcentaje de descuento', decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Detalle de factura'
        verbose_name_plural = 'Detalles de facturas'

    def __str__(self):
        return 'Detalle de la factura #' + str(self.invoice.number)