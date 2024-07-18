from odoo import models, fields, api

class SigninUser(models.Model):
    _name = 'sign.in.user'

    user_id = fields.Many2one('res.user', string="User")
    email = fields.Char(string="Email")
    password = fields.Char(string="Password")