from __future__ import absolute_import, unicode_literals
import io
import csv
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task()
def process_csv_file(token, csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',', skipinitialspace=True, quoting=csv.QUOTE_ALL)
        for row in reader:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                token,
                {
                    'type': 'send_message',
                    'message': dict(row)
                }
            )
    print(token)
    print(csv_file)