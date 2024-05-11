from odoo import fields, models, api, _
from odoo.exceptions import UserError

class CancelOrderWizard(models.TransientModel):
    _name = 'cancel.order.wizard'
    _description = "This is a notification before removing orders."

    password = fields.Char(string='Password')

    def cancel_order(self):
        expected_password = "janvi"  # Replace with your actual password
        if self.password == expected_password:
            active_ids = self.env.context.get('active_ids')
            orders = self.env['product.order'].browse(active_ids)
            orders.action_cancel()  # Call action_cancel to cancel the orders
            orders.write({'state': 'cancel'})  # Set the state of the orders to 'cancel'
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise UserError('Incorrect password! Please try again.')
            # If the password is incorrect, show an error message
            # return {
            #     'type': 'ir.actions.act_window',
            #     'res_model': 'cancel.order.wizard',
            #     'view_mode': 'form',
            #     'target': 'new',
            #     'context': {'default_password': _('Incorrect password! Please try again.')},
            # }