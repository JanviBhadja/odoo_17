from odoo import http
from odoo.http import request
import json

class saleOrderController(http.Controller):
    @http.route('/sale_order_search', type='http', auth="public", website=True, csrf=False, method=['get'])
    def sale_order_search(self, **post):
        sale_orders = post.get('sale_order')
        print(sale_orders)
        if sale_orders:
            sale_order = request.env['sale.order'].sudo().search([('name' ,'=', sale_orders)])
            print(sale_order)
            return request.render('custom_website.search_sale_order_details_template', {
                'sale_order': sale_order,
            })


