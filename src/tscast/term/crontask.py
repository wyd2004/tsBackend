
from .models import Order
from .models import Payment
from .models import Purchase
from wechat.api import wx_order_query

def payment_status_update():
    unchecked_payments = Payment.objects.filter(status='wait-for-payment')
    for wait_pay in unchecked_payments:
        state = wx_order_query()
        if state:
            wait_pay.status = 'succeeded'
        else:
            wait_pay.status = 'failed'
        wait_pay.save(force_update=True)

