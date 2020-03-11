from __future__ import absolute_import, unicode_literals
import io
import csv
import sys

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from invoices.models import UploadedFile, Invoice, InvoiceDetail


@shared_task()
def process_csv_file(id, token, csv_file, separator):
    with open(csv_file, 'r') as file:
        if 't' in separator:
            reader = csv.DictReader(file, delimiter='\t', skipinitialspace=True)

        else:
            reader = csv.DictReader(file, delimiter=separator, skipinitialspace=True)

        success_row = 0
        error_row = 0
        current_row = 1

        for row in reader:
            row_number_error = 0
            error_description = ''
            dict_row = dict(row)

            if len(list(reader.fieldnames)) != 9:

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    token,
                    {
                        'type': 'send_message',
                        'message': {
                            'success_rows': success_row,
                            'error_rows': error_row,
                            'row_number_error': 1,
                            'error_description': 'Es posible que el separador "'+ separator + '" no sea el correcto para el archivo.',
                            'id': id
                        }
                    }
                )

                break


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
            except ValueError as e:

                field_name = str(e).split(': ')[1]
                error_row += 1
                row_number_error = current_row

                row_data = list(dict_row.values())
                row_data_str = ','.join(row_data)

                error_description = 'Error al convertir el campo con valor: ' + field_name + " | " +row_data_str

            except KeyError as e:

                field_name = str(e)
                error_row += 1
                row_number_error = current_row

                row_data = list(reader.fieldnames)
                row_data_str = ', '.join(row_data)

                error_description = 'Error, no se encuentra la columna ' + field_name + "  | " + row_data_str

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