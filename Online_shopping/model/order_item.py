from odoo import models, fields , api , _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class OrderItem(models.Model):
    _name = 'order.item'
    _description = 'Order Item'
    _rec_name = 'order_id'

    order_id = fields.Many2one('product.order', string='Order', readonly=True)
    product_id = fields.Many2one('my.product.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string='Unit Price', related='product_id.price', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for item in self:
            print(item)
            print(self)
            item.price_subtotal = item.quantity * item.price_unit

    @api.constrains('quantity')
    def _check_quantity(self):
        for item in self:
            if item.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be positive.'),
    ]