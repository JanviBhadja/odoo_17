from datetime import timedelta
from odoo import models, fields, api

class Order(models.Model):
    _name = 'product.order'
    _description = 'Order'
    _rec_name = 'orderId'

    order_date = fields.Datetime(string='Order Date')
    customer_id = fields.Many2one('my.customer.customer', string='Customer')
    customer_email = fields.Char(string='Customer Email', related='customer_id.email', store=True)
    customer_address = fields.Text(string='Customer Address', related='customer_id.address', store=True)
    order_item_ids = fields.One2many('order.item', 'order_id', string='Order Items')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    orderId = fields.Char(string='Order Id', readonly=True, default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel','Cancel')], string='Status', default='draft')
    delivery_id = fields.Many2one('product.delivery.me' , string = 'Delivery ID' , readonly=True)
    payment_method = fields.Selection([
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('upi', 'UPI'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ], string='Payment Method')

    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ], string='Payment Status', compute='_compute_payment_status', store=True)

    def action_draft(self):
        # print(self)
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        # print(self)
        for rec in self:
            rec.state = 'confirmed'
        # self.write({'state': 'confirmed'})
    
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_done_success(self):
        self.write({'state': 'done',
                    'payment_status':'paid'})

    @api.depends('payment_method')
    def _compute_payment_status(self):
        for record in self:
            if record.payment_method == 'cash_on_delivery':
                record.payment_status = 'unpaid'
            else:
                record.payment_status = 'paid'
    
    @api.depends('order_item_ids')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order_item.price_subtotal for order_item in order.order_item_ids)
    
    @api.depends('order_item_ids')
    def _compute_order_item_count(self):
        for order in self:
            order.order_item_count = len(order.order_item_ids)

    @api.depends('order_item_ids')
    def _compute_order_item_details(self):
        for order in self:
            order.order_item_product_ids = order.order_item_ids.mapped('product_id')
            order.order_item_quantities = [(6, 0, order.order_item_ids.mapped('quantity'))]
            order.order_item_prices_unit = [(6, 0, order.order_item_ids.mapped('price_unit'))]
            order.order_item_subtotals = [(6, 0, order.order_item_ids.mapped('price_subtotal'))]

    @api.depends('order_item_ids')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order_item.price_subtotal for order_item in order.order_item_ids)


    @api.model
    def create(self, vals):
        vals['orderId'] = self.env['ir.sequence'].sudo().next_by_code('product.order') or 'New'
        res = super(Order,self).create(vals)
        return res
    
    @api.model
    def write(self, vals):
        res = super(Order, self).write(vals)
        # if self.state == 'confirmed':
        confirmed_orders = self.filtered(lambda order: order.state == 'confirmed')
        print('confirmed_orders',confirmed_orders)
        for order in confirmed_orders:
            print(confirmed_orders)
            # Check if a delivery record already exists for the order
            existing_delivery = self.env['product.delivery.me'].search([('order_id', '=', order.id)], limit=1)
            print('existing_delivery',existing_delivery)
            if existing_delivery:
                # Update the existing delivery record
                delivery_vals = {
                    'delivery_date': fields.Date.today() + timedelta(days=3),  # Set your expected delivery date here
                    'payment': 'paid' if order.payment_status == 'paid' else 'unpaid' , # Update payment status
                    'state' : 'ordered'
                }
                existing_delivery.write(delivery_vals)
                print('existing_delivery',existing_delivery)
            else:
                # Create a new product delivery record for each confirmed order
                self.env['product.delivery.me'].create({
                    'order_id': order.id,
                    'customer_id': order.customer_id.id,
                    'delivery_date': fields.Date.today() + timedelta(days=3),  # Set your expected delivery date here
                    'payment': 'paid' if order.payment_status == 'paid' else 'unpaid' , # Set payment status
                    'state' : 'ordered'
                })
            # query = """ALTER TABLE product_category_me DROP COLUMN create_uid"""
            query = """SELECT id FROM product_order"""
            self.env.cr.execute(query)
            order1 = self.env.cr.fetchall()
            print("order1------>", order1)
        return res

    def cancel_order(self):
        return {
            'name': 'Cancel Order',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.order.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

class OrderConfirmationButton(models.Model):
    _inherit = 'product.order'

    def confirm_order(self):
        self.action_confirm()
        return True
    
    def cancel_order(self):
        self.action_cancel()
        return True

    def cancel_order_wizard(self):
        return {
            'name': 'Cancel Order',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.order.wizard',
            'view_mode': 'form',
            'target': 'new',
        }