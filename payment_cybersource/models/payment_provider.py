# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
from datetime import datetime
import requests
from odoo import models, fields, api

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cybersource', "Cybersource")], ondelete={'cybersource': 'set default'})
    cybersource_merchant_id_key = fields.Char(
        string="Merchant Key")
    cybersource_api_key_id = fields.Char(
        string="API Key")
    cybersource_secret_key = fields.Char(
        string="Secret Key")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_signature(self, method, resource, time, digest):
        api_key_id = "f05d7f61-3f88-456c-b60f-2094b902c93a"
        secret_key = "yZHYkrivfG19ndGWsE3yohYfoJJZLW0SOEr9c0gA8dA="
        request_host = "apitest.cybersource.com"
        merchant_id = "janvi2403_1720528302"

        header_list = []
        header_list.append("keyid=\"" + str(api_key_id) + "\"")
        header_list.append(", algorithm=\"HmacSHA256\"")

        postheaders = "host date request-target digest v-c-merchant-id"
        header_list.append(", headers=\"" + postheaders + "\"")

        signature_list = []
        signature_list.append("host: " + request_host + "\n")
        signature_list.append("date: " + time + "\n")
        signature_list.append("request-target: " + method + " " + resource + "\n")
        signature_list.append("digest: SHA-256=" + digest + "\n")
        signature_list.append("v-c-merchant-id: " + merchant_id)

        sig_value = "".join(signature_list)
        sig_value_utf = bytes(sig_value, encoding='utf-8')

        secret = base64.b64decode(secret_key)
        hash_value = hmac.new(secret, sig_value_utf, hashlib.sha256)
        signature = base64.b64encode(hash_value.digest()).decode("utf-8")

        header_list.append(", signature=\"" + signature + "\"")
        token = ''.join(header_list)

        return token

    def get_digest(self, payload):
        hashobj = hashlib.sha256()
        hashobj.update(json.dumps(payload).encode('utf-8'))
        hash_data = hashobj.digest()
        digest = base64.b64encode(hash_data).decode('utf-8')
        return digest

    def perform_cybersource(self):
        payload = {
            "clientReferenceInformation": {
                "code": "TC50171_3"
            },
            "paymentInformation": {
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "12",
                    "expirationYear": "2031"
                }
            },
            "orderInformation": {
                "amountDetails": {
                    "totalAmount": "102.21",
                    "currency": "USD"
                },
                "billTo": {
                    "firstName": "John",
                    "lastName": "Doe",
                    "address1": "1 Market St",
                    "locality": "san francisco",
                    "administrativeArea": "CA",
                    "postalCode": "94105",
                    "country": "US",
                    "email": "test@cybs.com",
                    "phoneNumber": "4158880000"
                }
            }
        }

        digest = self.get_digest(payload)
        method = "post"
        resource = "https://apitest.cybersource.com/pts/v2/payments"
        current_time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        signature = self.get_signature(method, resource, current_time, digest)

        headers = {
            "v-c-merchant-id": "janvi2403_1720528302",
            "date": current_time,
            "host": "apitest.cybersource.com",
            "digest": "SHA-256=" + digest,
            "signature": signature,
            "content-type": "application/json",
            "Authorization": "Signature " + signature
        }

        response = requests.post(resource, json=payload, headers=headers)

        if response.status_code == 201:
            return response.json()
        else:
            return response.text
