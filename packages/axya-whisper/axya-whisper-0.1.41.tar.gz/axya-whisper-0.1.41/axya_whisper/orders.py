
import json
import logging 
import requests

from urllib.parse import quote
from io import BytesIO
from axya_whisper.auth import get_access_token
from axya_whisper.constants import AXYA_API_TOKEN, AXYA_API_URL, GENIUS_API_URL, GENIUS_PO_SENT_TYPE_ID, VERIFY_SSL, GeniusERPPurchaseOrderLineItemMapping, GeniusERPPurchaseOrderMapping
from axya_whisper.models import GeniusERPConfigurationResponse 

logger = logging.getLogger("axyawhisper.orders")
logger.setLevel(logging.DEBUG)

def fetch_purchase_orders(genius_config: GeniusERPConfigurationResponse):
    access_token = get_access_token()
    
    # Limit the fields returned
    fields = [
        GeniusERPPurchaseOrderMapping.name,
        GeniusERPPurchaseOrderMapping.vendor_id,
        GeniusERPPurchaseOrderMapping.delivery_date,
        GeniusERPPurchaseOrderMapping.updated_date,
        GeniusERPPurchaseOrderMapping.revision_date,
        GeniusERPPurchaseOrderMapping.note,
        GeniusERPPurchaseOrderMapping.created_at,
        GeniusERPPurchaseOrderMapping.status,
    ]

    filters = f"filter=PurchaseOrderTypeId={GENIUS_PO_SENT_TYPE_ID}"

    if genius_config.last_time_po_sync:
        encoded_last_sync = quote(f'"{genius_config.last_time_po_sync}"')
        filters = f"{filters}%26LastUpdate>{encoded_last_sync}"

    po_qs = f"{filters}&fields={';'.join(fields)}"
    headers = {"Authorization": f"Bearer {access_token}"}
    orders_endpoint = (
        f"{GENIUS_API_URL}/data/fetch/purchaseOrderHeaderEntity?{po_qs}"
    )

    response = requests.get(orders_endpoint, headers=headers)

    if response.status_code == 200:
        orders = response.json().get("Result")
        logger.info(f"{len(orders)} orders were found since last sync on {genius_config.last_time_po_sync}...")
        for order_info in orders:
            po_name = order_info.get(GeniusERPPurchaseOrderMapping.name)
            order_info["line_items"] =  fetch_po_line_items(genius_config, po_name)
            order_info["line_items"] = json.dumps(order_info["line_items"])
            po_file = fetch_po_pdf_report(genius_config, po_name)
            order_info["files"] = {"po_file": (f"po-{po_name}.pdf", po_file, 'application/pdf')}
        
        if len(orders) >= 1:
            sync_pos_with_axya(orders)

        return orders

def fetch_po_line_items(genius_config, po_code):

        # Limit the fields returned
    fields = [
        GeniusERPPurchaseOrderLineItemMapping.name,
        GeniusERPPurchaseOrderLineItemMapping.description,
        GeniusERPPurchaseOrderLineItemMapping.quantity,
        GeniusERPPurchaseOrderLineItemMapping.price,
        GeniusERPPurchaseOrderLineItemMapping.delivery_date,
    ]

    access_token = get_access_token()
    qs = f"filter=PurchaseOrderHeaderCode%3D{po_code}&fields={';'.join(fields)}"
    line_items_endpoint = (
        f"{GENIUS_API_URL}/data/fetch/purchaseOrderDetailEntity?{qs}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(line_items_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json().get("Result")
    
def fetch_po_pdf_report(genius_config, po_name):
    access_token = get_access_token()
    report_qs = f"?reportName=Commande&parameters=pCode%3D{po_name}"
    report_endpoint = (
        f"{GENIUS_API_URL}/report/STDRPTPURCHASEORDER/pdf?{report_qs}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(report_endpoint, headers=headers)
    logger.info("Fetching PDF report...")
    if response.status_code == 200:
        return response.content


def sync_pos_with_axya(orders):
    headers = {
        "Authorization": f"Token {AXYA_API_TOKEN}",
    }
    
    for order in orders:
       files = order.pop("files")
       response = requests.post(f"{AXYA_API_URL}/genius/poSync", data=order, files=files, headers=headers, verify=VERIFY_SSL)
       
       if response.status_code == 200:
           print("PO synced...")
       else:
           # Notify AXYA
           print("PO failed to sync...", response.status_code)

def get_update_purchase_orders():
    headers = {
        "Authorization": f"Token {AXYA_API_TOKEN}",
    }
    response = requests.get(f"{AXYA_API_URL}/genius/updatedPo", headers=headers, verify=VERIFY_SSL)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("line_items"):
            line_item_code = item.get("LineItemCode")
            po_code = item.get("Code")
            delivery_date = item.get("DateDelivery")
            line_item_id = get_line_item_pk_by_order_header(po_code, line_item_code)
            if line_item_id:
                print(f"updating delivery date for {po_code} -> {line_item_code} -> {delivery_date}")
                update_delivery_date(line_item_id, delivery_date)
    else:
        # Notify AXYA
        print("PO failed to sync...", response.status_code)


def get_line_item_pk_by_order_header(order_header_code, line_item_code):
    access_token = get_access_token()
    qs = f"filter=PurchaseOrderHeaderCode%3D{order_header_code}&fields=Id%3BItemCode"
    report_endpoint = (
        f"{GENIUS_API_URL}/data/fetch/purchaseOrderDetailEntity?{qs}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(report_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json().get("Result")
        id = None

        for item in data:
            if item.get("ItemCode") == line_item_code:
                id = item.get("Id")
        
        return id

def update_delivery_date(line_item_id, delivery_date):
    payload = { 
           "Id": line_item_id,
           "DateDelivery": delivery_date
    }
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = f"{GENIUS_API_URL}/data/single/purchaseOrderDetailEntity"
    response = requests.put(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        print("line item delivery date updated")
    else:
        print(f"Failed to update delivery date {response.status_code}")
