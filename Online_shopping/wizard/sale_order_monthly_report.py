from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import xlsxwriter
import io
from datetime import datetime, timedelta

class SaleReportScheduler(models.TransientModel):
    _name = 'sale.report.scheduler'
    _description = 'Sale Report Scheduler'

    # def excel_report_fetch_data(self):
        

    def generate_and_send_monthly_report(self):
        # Calculate dates for the previous month
        today = fields.Date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        start_date = first_day_of_previous_month.strftime('%Y-%m-%d')
        end_date = last_day_of_previous_month.strftime('%Y-%m-%d')
        print(">>>>>>>>>>>>",start_date,end_date)

        
        # Generate the report
        # report_data = self.env['commission.sale.wizard'].fetch_from_sale()
        if report_data:
            # Create the attachment
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            # Write your report data into the workbook here...

            workbook.close()
            output.seek(0)
            excel_file = output.read()
            output.close()

            attachment = self.env['ir.attachment'].create({
                'name': f'sales_report_from_{start_date}_to_{end_date}.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(excel_file),
                'res_model': 'sale.report.scheduler',
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            # Prepare email values
            email_values = {
                'subject': f"Monthly Sales Report ({start_date} to {end_date})",
                'attachment_ids': [(4, attachment.id)],
            }

            # Send email
            mail_template = self.env.ref('Online_shopping.mail_template_sale_report')  # Replace 'Your_Module' with your actual module name
            mail_template.send_mail(self.env.user.id, email_values=email_values, force_send=True)
        else:
            raise UserError("Failed to generate report or no data found for the previous month.")

    def action_send_email_with_report(self):
            report_data = self.generate_and_send_monthly_report()
            if report_data:
                attachment_data = {
                    'name': f'sales_report_from_{self.start_date}_to_{self.end_date}.xlsx',
                    'datas': base64.b64encode(report_data),
                    'datas_fname': f'sales_report_from_{self.start_date}_to_{self.end_date}.xlsx',
                    'res_model': 'commission.sale.wizard',
                    'res_id': self.id,
                }

                # Prepare email values
                email_values = {
                    'subject': f"Sales Report from {self.start_date} to {self.end_date}",
                    'body_html': '<p>Please find attached the sales report for the specified period.</p>',
                    'attachment_ids': [(0, 0, attachment_data)],
                }

                # Send email
                template_id = self.env.ref('Online_shopping.email_template_id').id  
                if template_id:
                    self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True, email_values=email_values)
                else:
                    raise ValueError("Email template not found.")
            else:
                raise ValueError("Failed to generate report data.")