from odoo import http
from odoo.http import request
import json

class ReportController(http.Controller):

    @http.route('/custom_report', type='json', auth='public')
    def generate_report(self, selected_data):
        # Generate the report based on the selected data
        report_data = {
            'report': 'Your report data here'
        }
        return json.dumps(report_data)
