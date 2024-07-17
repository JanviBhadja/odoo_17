from odoo import http
from odoo.http import request
import json


class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        print(kwargs)
        return request.render("custom_website.template_layout")

    @http.route('/myhome/user_data', type='http', auth='public', website=True, method=['post'])
    def data(self,**kwargs):
        data = kwargs.get('data')
        if request.env.user.name == "Public User":
            requst.env['public.user'].create({
                'email' : kwargs.get('email'),
                'password' : kwargs.get('password'),
            })
            return request.render("custom_website.template_status")
        else:
            requst.env['sign.in.user'].create({
                'user_id' : request.env.uid,
                'email' : kwargs.get('email'),
                'password' : kwargs.get('password'),
            })
            return request.render("custom_website.template_status")


    # @http.route('/myhome/create_sale_order', type='http', auth='public', website=True, method=['post'])
    # def create_sale_order(self, **kwargs):
    #     partner_id = kwargs.get('partner_id')
    #     user_id = kwargs.get('user_id')
    #     order_lines = http.loads(kwargs.get('order_lines', '[]'))

    #     if not partner_id or not user_id or not order_lines:
    #         return request.render("custom_website.template_status", {'status': 'error', 'message': 'Missing required fields'})

    #     sale_order = request.env['sale.order'].sudo().create({
    #         'partner_id': partner_id,
    #         'partner_invoice_id': partner_id,
    #         'partner_shipping_id': partner_id,
    #         'user_id': user_id,
    #         'order_line': [(0, 0, {
    #             'product_id': line['product_id'],
    #             'product_uom_qty': line['product_uom_qty'],
    #             'price_unit': line['price_unit'],
    #         }) for line in order_lines]
    #     })

    #     return request.render("custom_website.template_status", {
    #         'status': 'success',
    #         'sale_order': sale_order
    #     })