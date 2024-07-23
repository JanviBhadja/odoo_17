from odoo import models, fields, api

class PublicUser(models.Model):
    _name = 'public.user'
    _description = 'This is Public User'

    email = fields.Char(string="Email")
    password = fields.Char(string="Password")



# from odoo import models, fields, api
# from datetime import date

# class VolumeDiscount(models.Model):
#     _name = 'volume.discount'
#     _description = 'Volume Discount'

#     product_id = fields.Many2one('product.product', required=True, string='Product')
#     customer_id = fields.Many2one('res.partner', string='Customer')
#     min_quantity = fields.Integer(required=True, string='Minimum Quantity')
#     max_quantity = fields.Integer(string='Maximum Quantity')
#     discount_percentage = fields.Float(required=True, string='Discount Percentage')
#     start_date = fields.Date(string='Start Date')
#     end_date = fields.Date(string='End Date')

#     @api.model
#     def get_active_discounts(self, product_id, quantity, customer_id=None):
#         today = date.today()
#         domain = [
#             ('product_id', '=', product_id),
#             ('min_quantity', '<=', quantity),
#             ('start_date', '<=', today),
#             '|', ('end_date', '>=', today), ('end_date', '=', False),
#         ]
#         if customer_id:
#             domain.append(('customer_id', '=', customer_id))
#         return self.search(domain)
# from odoo import models, fields, api

# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'

#     volume_discount_applied = fields.Boolean(readonly=True, string='Volume Discount Applied')
#     discount_percentage = fields.Float(readonly=True, string='Discount Percentage')
#     discount_amount = fields.Monetary(readonly=True, string='Discount Amount')

#     @api.onchange('product_id', 'product_uom_qty')
#     def _apply_volume_discount(self):
#         for line in self:
#             if line.product_id and line.product_uom_qty:
#                 discounts = self.env['volume.discount'].get_active_discounts(
#                     product_id=line.product_id.id,
#                     quantity=line.product_uom_qty,
#                     customer_id=line.order_id.partner_id.id
#                 )
#                 if discounts:
#                     best_discount = max(discounts, key=lambda d: d.discount_percentage)
#                     line.volume_discount_applied = True
#                     line.discount_percentage = best_discount.discount_percentage
#                     line.discount_amount = line.price_unit  line.product_uom_qty  (best_discount.discount_percentage / 100)
#                     line.discount = best_discount.discount_percentage
#                 else:
#                     line.volume_discount_applied = False
#                     line.discount_percentage = 0.0
#                     line.discount_amount = 0.0
#                     line.discount = 0.0

# from odoo import models, fields, api

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'

#     total_discount = fields.Monetary(string='Total Discount', compute='_compute_total_discount')

#     @api.depends('order_line.discount_amount')
#     def _compute_total_discount(self):
#         for order in self:
#             order.total_discount = sum(order.order_line.mapped('discount_amount'))

#     @api.depends('order_line.price_total')
#     def _compute_amount(self):
#         super(SaleOrder, self)._compute_amount()
#         for order in self:
#             order.total_discount = sum(order.order_line.mapped('discount_amount'))
#             order.amount_total = order.amount_untaxed + order.amount_tax - order.total_discount



