from __future__ import absolute_import, unicode_literals
import io
import csv
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from invoices.models import UploadedFile, Invoice, InvoiceDetail


@shared_task()
def process_csv_file(id, token, csv_file, separator):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=separator, skipinitialspace=True, quoting=csv.QUOTE_ALL)

        success_row = 0
        error_row = 0
        current_row = 1

        for row in reader:
            row_number_error = 0
            error_description = ''
            dict_row = dict(row)
            try:
                invoice_obj, created = Invoice.objects.get_or_create(
                    number=dict_row['Número de factura'],
                    customer_name=dict_row['Nombres del cliente'],
                    customer_last_name=dict_row['Apellidos del cliente'],
                    customer_identification=dict_row['Identificación del cliente'],
                )

                detail_obj = InvoiceDetail.objects.create(
                    invoice=invoice_obj,
                    item_code=dict_row['Codigo del item'],
                    item_description=dict_row['Descripción del ítem'],
                    item_quantity=int(dict_row['Cantidad del ítem']),
                    unit_price=float(dict_row['Precio unitario']),
                    total_price=float(dict_row['Precio unitario']) * int(dict_row['Cantidad del ítem']),
                    discount_rate=float(dict_row['Número de factura']),

                )

                detail_obj.save()


                success_row += 1
            except Exception as e:
                error_row += 1
                row_number_error = current_row
                error_description = str(e)

            current_row += 1


            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                token,
                {
                    'type': 'send_message',
                    'message': {
                        'success_rows': success_row,
                        'error_rows': error_row,
                        'row_number_error': row_number_error,
                        'error_description': error_description,
                        'id': id
                    }
                }
            )

    UploadedFile.objects.get(pk=id).delete()