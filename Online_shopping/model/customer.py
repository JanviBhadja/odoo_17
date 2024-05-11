from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid

class Customer(models.Model):
    _name = 'my.customer.customer'
    _description = 'Customer'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    customerID = fields.Char(string='Customer Id', readonly=True, copy=False)
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count')
    order_ids = fields.One2many('product.order', 'customer_id', string='Orders')

    @api.depends('order_ids')
    def _compute_order_count(self):
        for rec in self:
            rec.order_count = len(rec.order_ids)

    def create(self, vals):
        print(vals)
        if vals.get('customerID', _('New')) == _('New'):
            vals['customerID'] = self._generate_customerID()
            print(vals['name'])
        return super(Customer, self).create(vals)
    
    def _generate_customerID(self):
        # Generate a random UUID
        return str(uuid.uuid4())

    @api.constrains('customerID')
    def _check_unique_customerID(self):
        print(self)
        for record in self:
            if record.customerID:
                existing_record = self.search([('customerID', '=', record.customerID)])
                if len(existing_record) > 1:
                    raise ValidationError("User ID must be unique.")

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.name:
                existing_record = self.search([('name', '=', record.name)])
                if len(existing_record) > 1:
                    raise ValidationError("User alredy exist.")

    def action_order_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Order',
            'res_model': 'product.order',
            'view_mode': 'tree,form,calendar',
            'target':'new',
            'domain': [('customer_id', '=', self.id)]
        }