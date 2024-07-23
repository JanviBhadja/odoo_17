from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    volume_discount_applied = fields.Boolean(string='Volume Discount Applied', compute='_compute_discount')
    discount_percentage = fields.Float(string='Discount Percentage', compute='_compute_discount')
    discount_amount = fields.Monetary(string='Discount Amount', compute='_compute_discount')

    @api.depends('product_id', 'product_uom_qty', 'order_id.partner_id')
    def _compute_discount(self):
        for line in self:
            discounts = self.env['volume.discount'].get_active_discounts(line.product_id.id, line.product_uom_qty, line.order_id.partner_id.id)
            if discounts:
                line.discount_percentage = discounts[0].discount_percentage
                line.volume_discount_applied = True
                line.discount_amount = (line.price_unit * line.product_uom_qty) * (line.discount_percentage / 100)
            else:
                line.discount_percentage = 0.0
                line.volume_discount_applied = False
                line.discount_amount = 0.0
