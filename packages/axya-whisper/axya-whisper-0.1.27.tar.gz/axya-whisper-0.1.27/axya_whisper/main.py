import os
import requests
import sys
import logging

sys.path.append('C:\\Users\\Axya1\\Documents\\axya-sync')

from axya_whisper.orders import fetch_purchase_orders, get_update_purchase_orders
from axya_whisper.config import get_axya_config



logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def service():
    genius_config = get_axya_config()

    if genius_config.fetch_sent_purchase_orders_enabled:
        orders = fetch_purchase_orders(genius_config)
    if genius_config.auto_sync_updated_delivery_dates:
        get_update_purchase_orders()

if __name__ == "__main__":
    service()