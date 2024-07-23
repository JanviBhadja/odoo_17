from odoo import models, fields
from datetime import date

class VolumeDiscount(models.Model):
    _name = 'volume.discount'
    _description = 'Volume Discount Model'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', help='Optional field for customer specific discount')
    min_quantity = fields.Integer(string='Minimum Qty', required=True)
    max_quantity = fields.Integer(string='Maximum Qty')
    discount_percentage = fields.Float(string='Discount Percentage', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def get_active_discounts(self, product_id, quantity, customer_id=None):
        today = date.today()
        domain = [
            ('product_id', '=', product_id),
            ('min_quantity', '<=', quantity),
            ('start_date', '<=', today),
            '|', ('end_date', '>=', today), ('end_date', '=', False),
        ]
        if customer_id:
            domain.append(('customer_id', '=', customer_id))
        return self.search(domain)
