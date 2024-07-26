from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_amount_total = fields.Float(string='Total Discount Amount', compute='_compute_discount_amount_total')

    @api.depends('order_line.discount_amount')
    def _compute_discount_amount_total(self):
        for order in self:
            order.discount_amount_total = sum(order.order_line.mapped('discount_amount'))
        
    @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total','discount_amount_total')
    def _compute_amounts(self):
        super(SaleOrder, self)._compute_amounts()
        print("<<<<<<<<<<<<<Hello>>>>>>>>>>>>>>>")
        for order in self:
            order.amount_total -= order.discount_amount_total
            print(order.amount_total)
            return order

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.volume_discount_applied:
                    vals = {
                        'sale_order_id': order.id,
                        'line_id': line.id,
                        'discount_percentage': line.discount_percentage,
                        'discount_amount': line.discount_amount,
                        'timestamp': fields.Datetime.now(),
                    }
                    self.env['discount.history.tracking'].create(vals)
        return res