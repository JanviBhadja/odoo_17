from odoo import http
from odoo.http import request
import json


class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        print(kwargs)
        return request.render("custom_website.template_layout")

    @http.route('/myhome/submited', type='http', auth='public', website=True)
    def status(self,**kwargs):
        status = kwargs.get('status')
        if status == "success":
            return request.render("custom_website.template_status")