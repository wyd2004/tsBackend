import json
from .models import Order
from .models import Payment
from .models import Purchase
from wechat.api import wx_order_query

def payment_status_update():
    unchecked_payments = Payment.objects.filter(status='wait-for-payment')
    for wait_pay in unchecked_payments:
        if not wait_pay.receipt:
            continue
        pay_receipt = json.loads(wait_pay.receipt)
        nonce_str = pay_receipt['prepay']['nonce_str']
        out_trade_no = pay_receipt['prepay']['out_trade_no']
        sign = pay_receipt['prepay']['sign']
        state = wx_order_query(nonce_str, out_trade_no, sign)
        if state:
            wait_pay.status = 'succeeded'
        else:
            wait_pay.status = 'failed'
        wait_pay.save(force_update=True)
        Order.objects.filter(uuid=wait_pay.uuid).update(
            status=wait_pay.status
        )

