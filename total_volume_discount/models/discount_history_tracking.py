from odoo import models, fields

class DiscountHistoryTracking(models.Model):
    _name = 'discount.history.tracking'
    _discription = 'Discount History Tracking'

    
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    line_id = fields.Many2one('sale.order.line', string='Sale Order Line', required=True)
    discount_percentage  = fields.Float(string='Discount Percentage', required=True)
    discount_amount = fields.Monetary(string='Discounted Amount', required=True)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id)
    timestamp = fields.Datetime(string='Discount Time',required=True)
    
    