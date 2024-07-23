from odoo import http
from odoo.http import request
import json


class myMain(http.Controller):

    # custom menu route
    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        print(kwargs)
        return request.render("custom_website.template_layout")

    # sale order table route
    @http.route('/shopping/hello', type='http', auth='public', website=True)
    def sale_order(self, **kwargs):
        customers = request.env['sale.order'].search([])
        return request.redirect("custom_website.sale_order",{
            'sale_data': customers
        })

    # submit form route
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

    # select sale order dropdown
    @http.route(['/sale_order_snippet'], type='json', auth="public", website=True)
    def sale_order_snippet(self):
        sale_orders = request.env['sale.order'].search([])
        print('sale_orders:', sale_orders)
        values = {
            'sale_orders': sale_orders,
        }
        print('values:', values)
        return request.render('custom_website.sale_order_form_snippet_my', values)

    # @http.route('/sale_order_table', type='http', auth='public', website=True)
    # def sale_order_table(self, **kwargs):
    #     orders = request.env['sale.order'].sudo().search([])
    #     return request.render('custom_website.sale_order_table_page', {'orders': orders})
