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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    extra_tags = fields.Char(string="extra_tags")

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'extra_tags': self.extra_tags
        })
        return values


class writeAnotherDetail(models.Model):
    _inherit="stock.move"

    extra_tags = fields.Char(string = "Extra field", help="enter the date when order was placed")

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['extra_tags']
        return fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # commission = fields.Float(string="Commission", compute="compute_commision_amount")
    
    # @api.depends("amount_total")
    # def compute_commision_amount(self):
    #     for i in self:
    #         i.commission = (i.amount_total*5)/100

    commission = fields.Float(string="Commission", compute="compute_commision_amount")
    
    @api.depends("amount_total", "partner_id.commission_amount_on", "partner_id.percentage")
    def compute_commision_amount(self):
        for order in self:
            if order.amount_total > order.partner_id.commission_amount_on:
                order.commission = (order.amount_total * order.partner_id.percentage) / 100
            else:
                order.commission = 0.0

    commission_order_id = fields.Many2one('commission.on.line', string='Commission Order', readonly=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.commission_order_id:
            self.commission_order_id.write({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': self.commission,
                'total': self.amount_total,
            })
        else:
            commission_order = self.env['commission.on.line'].create({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': self.commission,
                'total': self.amount_total,
            })
            self.commission_order_id = commission_order.id
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if self.commission_order_id:
            self.commission_order_id.unlink()
        return res

    checking_date = fields.Date(string = "Ordering Date", help="enter the date when order was placed")

    nick_name = fields.Char(string="Nick Name")

    def action_generate_sale_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate Sale Report',
            'res_model': 'sale.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }

    @api.model

    def _get_order_lines_to_report(self):
        order_lines_context = self.env.context.get('order_lines')
        if order_lines_context:
            return self.order_line.filtered(lambda l: l.id in order_lines_context)
        return super(SaleOrder, self)._get_order_lines_to_report()



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nick_name = fields.Char(string="Nick Name", readonly=True,related='sale_id.nick_name'
    )

#     class CustomStockQuant(models.Model):
#     _inherit = 'stock.quant'

#     @api.model
#     def _get_available_quantity(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False, allow_negative=False):
#         print("<<<<<<<<<<<<<<<<<<<<_get_available_quantity>>>>>>>>>>>>>")
#         available_quantity = super(CustomStockQuant, self)._get_available_quantity(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict, allow_negative=allow_negative)
#         print(available_quantity)
#         if available_quantity <= 0:
#             raise UserError(_('Error: Available quantity is zero!'))

#         return available_quantity