# encoding: utf-8
success_payload = '''
        <xml>
          <appid><![CDATA[wx2421b1c4370ec43b]]></appid>
          <attach><![CDATA[支付测试]]></attach>
          <bank_type><![CDATA[CFT]]></bank_type>
          <fee_type><![CDATA[CNY]]></fee_type>
          <is_subscribe><![CDATA[Y]]></is_subscribe>
          <mch_id><![CDATA[10000100]]></mch_id>
          <nonce_str><![CDATA[5d2b6c2a8db53831f7eda20af46e531c]]></nonce_str>
          <openid><![CDATA[oUpF8uMEb4qRXf22hE3X68TekukE]]></openid>
          <out_trade_no><![CDATA[5383e3baa9714c6ab19b3a39b66e6bab]]></out_trade_no>
          <result_code><![CDATA[SUCCESS]]></result_code>
          <return_code><![CDATA[SUCCESS]]></return_code>
          <sign><![CDATA[B552ED6B279343CB493C5DD0D78AB241]]></sign>
          <sub_mch_id><![CDATA[10000100]]></sub_mch_id>
          <time_end><![CDATA[20140903131540]]></time_end>
          <total_fee>1</total_fee>
          <trade_type><![CDATA[JSAPI]]></trade_type>
          <transaction_id><![CDATA[1004400740201409030005092168]]></transaction_id>
        </xml>
    '''


fail_payload = '''
        <xml>
          <return_code><![CDATA[FAIL]]></return_code>
        </xml>
    '''

import requests
url = 'http://127.0.0.1:8000/api/wechat/wxpay/notify/'
res = requests.post(url, data=success_payload)
print res.content
res = requests.post(url, data=fail_payload)
print res.content
