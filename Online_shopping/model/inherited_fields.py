from odoo import models, fields, api

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
            if order.amount_total > order.user_id.partner_id.commission_amount_on:
                order.commission = (order.amount_total * order.user_id.partner_id.percentage) / 100
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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commission_amount_on = fields.Float(string='Commission Amount On')
    percentage = fields.Float(string="Percentage")
    dob = fields.Date(string='Date of Birth')

    def action_send_email(self):
        self.ensure_one()
        mail_template = self.env.ref('Online_shopping.mail_res_partner_template_blog')
        ctx = {
            'default_model': 'res.partner',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,

        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    # @api.model
    # def bday_notification(self):
    #     # for rec in self:
    #     # print("ASDE")
    #     try:
    #         records = self.env['res.partner'].search([('dob','=',fields.Date.today())])

    #         for rec in records:
    #                         email_values = {
    #                             'email_to': rec
    #                             .email,
    #                             'subject': "Happy Birthday",
    #                             # 'body_html': "<div><p>Wishing you a very happy birthday!</p></div>"
    #                             }
    #         mail_template = self.env.ref('Online_shopping.renew_bday_template')
    #         mail_template.with_context({}).send_mail(rec.id, email_values=email_values, force_send=True)
    #         print("Successfully Send a Email For Bday wishes")
            
    #     except Exception as e:
    #         print(e)


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