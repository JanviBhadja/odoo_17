from odoo import http
from odoo.http import request
import json


class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        print(kwargs)
        return request.render("custom_website.template_layout")

    @http.route('/shopping/hello', type='http', auth='public', website=True)
    def sale_order(self, **kwargs):
        customers = request.env['sale.order'].search([])
        return request.redirect("custom_website.sale_order",{
            'sale_data': customers
        })

    @http.route('/myhome/user_data', type='http', auth='public', website=True, method=['post'])
    def data(self,**kwargs):
        data = kwargs.get('data')
        print(request.env.user.name)
        if request.env.user.name == "Public user":
            request.env['public.user'].create({
                'email' : kwargs.get('email'),
                'password' : kwargs.get('password'),
            })
            return request.redirect("/myhome")
        else:
            request.env['sign.in.user'].create({
                'user_id' : request.env.uid,
                'email' : kwargs.get('email'),
                'password' : kwargs.get('password'),
            })
            return request.redirect("/shopping/hello")


    # @http.route('/myhome/create_sale_order', type='http', auth='public', website=True, method=['post'])
    # def create_sale_order(self, **kwargs):
    #     partner_id = kwargs.get('partner_id')
    #     user_id = kwargs.get('user_id')
    #     order_lines = http.json.loads(kwargs.get('order_lines', '[]'))

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