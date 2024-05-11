from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Product(models.Model):
    _name = 'my.product.product'
    _description = 'Product'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True)
    category_id = fields.Many2one('product.category.me', string='Category')
    image = fields.Binary(string='Image')
    productId = fields.Char(string='Product Id' , readonly=True, copy=False)

    @api.model
    def create(self, vals):
        print(self)
        vals['productId'] = self.env['ir.sequence'].sudo().next_by_code('my.product.product') or 'New'
        res = super(Product,self).create(vals)
        return res

    @api.constrains('price')
    def _check_price(self):
        for product in self:
            if product.price <= 0:
                raise ValidationError("Price must be greater than zero.")