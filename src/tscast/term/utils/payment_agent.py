import json

class WeChatPayment(object):
    # wechat payment
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=7_4
    # * step 0, client request server create order
    # * step 1.0 server generate vendor payment after create order
    # * step 1.1 server request wechat peyment getway get a prepay_id
    # * step 1.2 server generate a pay_sign
    # * step 1.3 server response client the pay_sign and prepay_id
    # * step 2.0 server receive a info from wechat server
    # * step 2.1 server handle the payment, and order
    # * step 2.2 server info wechat server handle result
    # end

    def __init__(self, payment):
        self.payment = payment

    def loads_receipt(self):
        if payment.receipt:
            self.receipt = json.loads(payment.receipt)
        else:
            self.receipt = {}

    def dumps_receipt(self):
        receipt = json.dumps(self.receipt)
        payment.receipt = receipt
        payment.save()

    def handle_init(self):
        kw = {}
        self.receipt = {}
        self.receipt['init'] = kw

    def handle_prepare(self):
        init_kw = self.receipt.get('init', {})
        kw = {}
        self.receipt['prepare'] = kw

    def handle_callback(self):
        return 
    
    def get_init(self):
        return self.receipt.get('init', {})

    def set_init(self, kw):
        self.receipt['init'] = kw

    def get_prepare(self):
        return self.receipt.get('prepare', {})

    def set_prepare(self, kw):
        self.receipt['prepare'] = kw
    
    def get_callback(self):
        return self.receipt.get('callback', {})

    def set_callback(self, kw):
        self.receipt['callback'] = kw
