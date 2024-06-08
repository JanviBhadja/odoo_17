from odoo import http
from odoo.http import request
import json

class ReportController(http.Controller):

    @http.route('/custom_report', type='json', auth='public')
    def generate_report(self, selected_data):
        report_data = {
            'report': ''
        }
        return json.dumps(report_data)
