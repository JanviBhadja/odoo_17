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
