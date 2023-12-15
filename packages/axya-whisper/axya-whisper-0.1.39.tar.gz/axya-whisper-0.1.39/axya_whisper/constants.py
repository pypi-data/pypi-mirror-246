import os 

VERIFY_SSL = False
SERVICE_CACHE_KEY = "GENIUS_API_TOKEN"
GENIUS_API_URL = os.environ.get('GENIUS_API_URL') 
GENIUS_API_LOGIN = os.environ.get('GENIUS_API_LOGIN')
GENIUS_API_PASSWORD = os.environ.get('GENIUS_API_PASSWORD')
GENIUS_API_COMPANY_CODE = os.environ.get('GENIUS_API_COMPANY_CODE')
AXYA_API_URL = os.environ.get('AXYA_API_URL')
AXYA_API_TOKEN = os.environ.get('AXYA_API_TOKEN')


GENIUS_PO_SENT_TYPE_ID = os.environ.get('GENIUS_PO_SENT_STATUS_ID', 11)


class GeniusERPPurchaseOrderMapping:
    name = "Code"
    vendor_id = "PaidToVendorCode"
    updated_date = "LastUpdate"
    delivery_date = "DeliveryDate"
    revision_date = "RevisionDate"
    created_at = "PurchaseDate"
    note = "QuickNote"
    status = "PurchaseOrderTypeId"


class GeniusERPPurchaseOrderLineItemMapping:
    name = "ItemCode"
    price = "Price"
    quantity = "QtyOrdered"
    delivery_date = "DateDelivery"
    updated_delivery_date = "VendorSuggestedDeliveryDate"
    confirmation_date = "VendorConfirmationDate"
    created_at = "PurchaseDate"
    description = "FullSearch"