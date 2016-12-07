from django.test import TestCase

import uuid

from .api import create_wxpay_prepay

class WeChatAPITestCase(TestCase):
    def setUP(self):
        pass

    def test_wxpay_prepay(self):
        openid = 'oGLrdvhFeahPIst52PdqknXgulq0'
        notify_url = 'http://ts.asyn.me/api/term/payment_callback'
        ip = '240.1.2.193'
        kwargs = {
                'title': 'test prepay',
                'attach': None,
                'order_id': uuid.uuid4().get_hex(),
                'fee': 3,
                'client_ip': ip,
                'notify_url': notify_url,
                'product_id': 2,
                'open_id': openid,
                }
        prepay = create_wxpay_prepay(**kwargs)
        self.assertIn('return_code', prepay)
        self.assertIn('return_msg', prepay)
        self.assertIn('appid', prepay)
        self.assertIn('mch_id', prepay)
        self.assertIn('device_info', prepay)
        self.assertIn('nonce_str', prepay)
        self.assertIn('result_code', prepay)
        self.assertIn('prepay_id', prepay)
        self.assertIn('trade_type', prepay)
