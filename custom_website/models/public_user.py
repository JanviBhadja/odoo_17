from odoo import models, fields, api

class PublicUser(models.Model):
    _name = 'public.user'

    email = fields.Char(string="Email")
    password = fields.Char(string="Password")
    