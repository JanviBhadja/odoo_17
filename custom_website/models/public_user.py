from odoo import models, fields, api

class PublicUser(models.Model):
    _name = 'public.user'
    _description = 'This is Public User'

    email = fields.Char(string="Email")
    password = fields.Char(string="Password")



