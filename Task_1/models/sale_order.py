from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Discount Sale order"

