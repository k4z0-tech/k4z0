"""
Configuration for Order Analysis Agent
"""

# Default settings
DEFAULT_TAT_THRESHOLD_DAYS = 3
DATA_FILE = "order_train_data.xlsx"
FEEDBACK_FILE = "feedback_history.json"

# Column name mappings (case-insensitive)
COLUMN_MAPPINGS = {
    'order_id': ['order id', 'order_id', 'orderid', 'order number'],
    'delivery_tat': ['delivery tat', 'delivery_tat', 'deliverytat', 'tat'],
    'status': ['status', 'order status'],
    'customer': ['customer', 'customer name', 'customername'],
    'product': ['product', 'product name', 'productname'],
    'order_date': ['order date', 'orderdate', 'date'],
    'delivery_date': ['delivery date', 'deliverydate']
}

# Success rate thresholds
SUCCESS_RATE_THRESHOLDS = {
    'high': 70,
    'medium': 40,
    'low': 0
}

# Feedback categories
DELAY_REASONS = [
    'Stock unavailability',
    'Logistics delay',
    'Customs clearance',
    'Quality check failed',
    'Customer request',
    'Payment issues',
    'Address issues',
    'Weather conditions',
    'Supplier delay',
    'Other'
]

ACTION_CATEGORIES = [
    'Contacted supplier',
    'Escalated to management',
    'Offered discount',
    'Changed shipping method',
    'Updated delivery address',
    'Expedited processing',
    'Arranged pickup',
    'Provided alternative product',
    'Extended delivery window',
    'Other'
]
