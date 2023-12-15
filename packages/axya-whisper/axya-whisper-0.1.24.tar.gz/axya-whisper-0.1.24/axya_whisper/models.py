import logging
from datetime import datetime

logger = logging.getLogger("axyawhisper.models")


class GeniusERPConfigurationResponse:
    def __init__(self, response_data):
        self.id = response_data.get('id')
        self.created_at = response_data.get('created_at')
        self.updated_at = response_data.get('updated_at')
        self.suppliers_filter = response_data.get('suppliers_filter')
        self.auto_send_po = response_data.get('auto_send_po')
        self.auto_archive_purchase_order = response_data.get('auto_archive_purchase_order')
        self.fetch_sent_purchase_orders_enabled = response_data.get('fetch_sent_purchase_orders_enabled')
        self.fetch_po_statuses_enabled = response_data.get('fetch_po_statuses_enabled')
        self.fetch_po_buyers_enabled = response_data.get('fetch_po_buyers_enabled')
        self.auto_sync_updated_delivery_dates = response_data.get('auto_sync_updated_delivery_dates')
        self.auto_sync_line_item_status = response_data.get('auto_sync_line_item_status')
        self.created_by = response_data.get('created_by')
        self.updated_by = response_data.get('updated_by')
        self.company = response_data.get('company')

        self.last_time_po_sync = self.format_datetime(response_data.get('last_time_po_sync'))
        self.last_time_suppliers_sync = self.format_datetime(response_data.get('last_time_suppliers_sync'))
        self.last_time_buyers_sync = self.format_datetime(response_data.get('last_time_buyers_sync'))

    def format_datetime(self, date_str):
        print(date_str)
        if date_str:
            try:
                # Attempt to parse with microseconds and timezone
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                try:
                    # Attempt to parse without microseconds and timezone
                    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    # If parsing fails, return None
                    logger.info("ValueError: {date_str}")
                    return None
            print("dt:", dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
            return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        return None