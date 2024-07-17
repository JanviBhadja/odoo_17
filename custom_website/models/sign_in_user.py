from odoo import models, fields, api

class SigninUser(models.Model):
    _name = 'sign.in.user'

    email = fields.Char(string="Email")
    password = fields.Char(string="Password")