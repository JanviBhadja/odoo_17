# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import requests
from datetime import datetime
import time
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

        header_list = [
            f'keyid="{api_key_id}"',
            'algorithm="HmacSHA256"',
            'headers="host date request-target digest v-c-merchant-id"'
        ]

        signature_list = [
            f'host: {request_host}',
            f'date: {time}',
            f'request-target: {method} {resource}',
            f'digest: SHA-256={digest}',
            f'v-c-merchant-id: {merchant_id}'
        ]

        sig_value = "\n".join(signature_list)
        sig_value_utf = sig_value.encode('utf-8')
        secret = base64.b64decode(secret_key)
        hash_value = hmac.new(secret, sig_value_utf, hashlib.sha256)
        signature = base64.b64encode(hash_value.digest()).decode("utf-8")

        header_list.append(f'signature="{signature}"')
        token = ", ".join(header_list)

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
        base_url = "https://apitest.cybersource.com/pts/v2/payments"
        resource = "/pts/v2/payments"
        current_time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        signature = self.get_signature(method, resource, current_time, digest)

        headers = {
            'host': "apitest.cybersource.com",
            'date': current_time,
            'digest': f"SHA-256={digest}",
            'v-c-merchant-id': "janvi2403_1720528302",
            'signature': signature,
            'Content-Type': 'application/json'
        }

        print("Payload:", json.dumps(payload, indent=4))
        print("Headers:", headers)

        response = requests.post(base_url, json=payload, headers=headers)

        print("Response Status:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 201:
            return response.json()
        else:
            return response.text