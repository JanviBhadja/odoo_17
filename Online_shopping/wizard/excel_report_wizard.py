from odoo import api, fields, models
import io
import xlsxwriter
import base64

class CommissionWizard(models.TransientModel):
    _name = 'commission.sale.wizard'
    _description = 'Commission Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def fetch_from_sale(self):
        domain = [
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),  
        ]
        action = self.env['sale.order'].search(domain)
        return action

    def action_xlsx_report_download(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Sales Report')

        # Define styles
        bold_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 
            'bg_color': '#FF5733', 'border': True, 'text_wrap': True
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 12, 'valign': 'vcenter', 
            'bg_color': '#FFEB3B', 'font_color': '#FFFFFF', 'border': True, 'text_wrap': True
        })
        normal_format = workbook.add_format({
            'text_wrap': True, 'align': 'left', 'valign': 'top', 'border': True
        })
        number_format = workbook.add_format({
            'num_format': '0.00', 'text_wrap': True, 'align': 'left', 'border': True
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy', 'align': 'left', 'valign': 'top', 'border': True
        })
        total_format = workbook.add_format({
            'bold': True, 'bg_color': '#FFEB3B', 'border': True  # Yellow background for totals
        })

        # Set column sizes
        sheet.set_column('A:A', 7)
        sheet.set_column('B:C',13)
        sheet.set_column('D:E',15)
        sheet.set_column('F:F',10)
        sheet.set_column('G:G',25)
        sheet.set_column('H:K',12)
        sheet.set_column('N:N',10)
        sheet.set_column('O:O',10)
        sheet.set_default_row(20)  # Adjust the height as needed
        sheet.set_row(0, 30)

        # Write report header
        report_header = f"Sales Report from {self.start_date.strftime('%d-%m-%Y')} to {self.end_date.strftime('%d-%m-%Y')}"
        sheet.merge_range('A1:O1', report_header, header_format)
        sheet.set_row(0, 25)  # Set row height for the header
        sheet.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'Number', 'Order Date', 'Expected date', 'Customer', 'Salesperson', 'Sales Team', 'Company',
            'Untaxed amount', 'Taxes', 'Amount Total', 'Tags', 'Status', 'Delivery status', 'Invoice status',
            'Amount to invoice'
        ]
        for i, header in enumerate(headers):
            sheet.write(1, i, header, bold_format)

        data = self.fetch_from_sale()
        row = 2  # Start from the third row

        # Initialize column totals
        column_totals = [0] * 4  # Columns H, I, J,O

        for rec in data:
            currency_symbol = rec.currency_id.symbol if rec.currency_id else ''
            sheet.write(row, 0, (rec.name or '').capitalize(), number_format)
            sheet.write(row, 1, rec.date_order.strftime('%d-%m-%y') if rec.date_order else 'Na', date_format)
            sheet.write(row, 2, rec.expected_date.strftime('%d-%m-%y') if rec.expected_date else 'Na', date_format)
            sheet.write(row, 3, (rec.partner_id.name or '').capitalize(), normal_format)
            sheet.write(row, 4, (rec.user_id.name or '').capitalize(), normal_format)
            sheet.write(row, 5, (rec.team_id.name or '').capitalize(), normal_format)
            sheet.write(row, 6, (rec.company_id.name or '').capitalize(), normal_format)
            sheet.write(row, 7, f"{currency_symbol}{round(rec.amount_untaxed,2) or 'NA'}", number_format)
            sheet.write(row, 8, f"{currency_symbol}{round(rec.amount_tax,2) or 'NA'}", number_format)
            sheet.write(row, 9, f"{currency_symbol}{round(rec.amount_total,2) or 'NA'}", number_format)
            sheet.write(row, 10, ', '.join(tag.name.capitalize() for tag in rec.tag_ids) or 'NA', normal_format)
            sheet.write(row, 11, (rec.state or 'NA').capitalize(), normal_format)
            sheet.write(row, 12, (rec.delivery_status or 'NA').capitalize(), normal_format)
            sheet.write(row, 13, (rec.invoice_status or 'NA').capitalize(), normal_format)
            sheet.write(row, 14, f"{currency_symbol}{round(rec.amount_to_invoice,2) or 'NA'}", number_format)

            # Update column totals
            column_totals[0] += rec.amount_untaxed or 0
            column_totals[1] += rec.amount_tax or 0
            column_totals[2] += rec.amount_total or 0
            column_totals[3] += rec.amount_to_invoice or 0

            # Apply conditional formatting based on state
            if rec.state == 'sale':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#90EE90'}))  # Light green for sale
            elif rec.state == 'draft':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#ECFF33'}))  # Light yellow for draft
            elif rec.state == 'cancel':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#FFA07A'}))  # Light salmon for cancel
            row += 1

        # Write totals at the bottom
        sheet.write(row, 6, 'Total', total_format)
        sheet.write(row, 7, f"{currency_symbol}{round(column_totals[0],2)}", total_format)
        sheet.write(row, 8, f"{currency_symbol}{round(column_totals[1],2)}", total_format)
        sheet.write(row, 9, f"{currency_symbol}{round(column_totals[2],2)}", total_format)
        sheet.write(row, 14, f"{currency_symbol}{round(column_totals[3],2)}", total_format)
        
        
        sheet1 = workbook.add_worksheet('Customer Report')
        
        bold_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 
            'bg_color': '#FF5733', 'border': True, 'text_wrap': True
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 12, 'valign': 'vcenter', 
            'bg_color': '#FFEB3B', 'font_color': '#FFFFFF', 'border': True, 'text_wrap': True
        })
        normal_format = workbook.add_format({
            'text_wrap': True, 'align': 'left', 'valign': 'top', 'border': True
        })
        number_format = workbook.add_format({
            'num_format': '0.00', 'text_wrap': True, 'align': 'left', 'valign': 'top', 'border': True
        })
        total_format = workbook.add_format({
            'bold': True, 'bg_color': '#FFEB3B', 'border': True  # Yellow background for totals
        })
        
        
        sheet1.set_column('A:A',20)
        sheet1.set_column('B:E',15)
        sheet1.set_default_row(20)  
        sheet1.set_row(0, 30)
        
        sheet1.merge_range('A1:F1', report_header, header_format)
        sheet1.set_row(0, 25)  # Set row height for the header
        sheet1.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'Customer', 'Untaxed amount', 'Taxes', 'Amount Total', 'Amount to invoice', 'Total'
        ]
        # for i, header in enumerate(headers):
        #     sheet1.write(1, i, header, bold_format)

        # domain = [
        #     ('date_order', '>=', self.start_date),
        #     ('date_order', '<=', self.end_date),
        # ]
        # customer_data = self.env['sale.order'].read_group(domain, ['amount_untaxed', 'amount_tax', 'amount_total', 'amount_to_invoice'], ['partner_id'])
        # row = 2  # Start from the third row 

        for i, header in enumerate(headers):
            sheet1.write(1, i, header, bold_format)

        query = """
        SELECT so.partner_id, 
               SUM(so.amount_untaxed) AS amount_untaxed,
               SUM(so.amount_tax) AS amount_tax,
               SUM(so.amount_total) AS amount_total,
               SUM(so.amount_to_invoice) AS amount_to_invoice
            FROM sale_order so
            WHERE so.date_order >= %s AND so.date_order <= %s
            GROUP BY so.partner_id
        """
        self.env.cr.execute(query, (self.start_date, self.end_date))
        results = self.env.cr.fetchall()

        row = 2  # Start from the second row for data
        for result in results:
            partner_id = result[0]
            amount_untaxed = result[1]
            amount_tax = result[2]
            amount_total = result[3]
            amount_to_invoice = result[4]

            # Get partner name using partner_id
            partner_name = self.env['res.partner'].browse(partner_id).name

            # Write data to the worksheet
            sheet1.write(row, 0, partner_name, normal_format)
            sheet1.write(row, 1, f"{currency_symbol}{round(amount_untaxed, 2)}", number_format)
            sheet1.write(row, 2, f"{currency_symbol}{round(amount_tax, 2)}", number_format)
            sheet1.write(row, 3, f"{currency_symbol}{round(amount_total, 2)}", number_format)
            sheet1.write(row, 4, f"{currency_symbol}{round(amount_to_invoice, 2)}", number_format)

            row += 1
      
        # for rec in customer_data:
        #     partner_name = self.env['res.partner'].browse(rec['partner_id'][0]).name
        #     amount_untaxed = rec.get('amount_untaxed', 0)
        #     amount_tax = rec.get('amount_tax', 0)
        #     amount_total = rec.get('amount_total', 0)
        #     amount_to_invoice = rec.get('amount_to_invoice', 0)

        #     sheet1.write(row, 0, partner_name, normal_format)
        #     sheet1.write(row, 1, f"{currency_symbol}{amount_untaxed or 'NA'}", number_format)
        #     sheet1.write(row, 2, f"{currency_symbol}{amount_tax or 'NA'}", number_format)
        #     sheet1.write(row, 3, f"{currency_symbol}{amount_total or 'NA'}", number_format)
        #     sheet1.write(row, 4, f"{currency_symbol}{amount_to_invoice or 'NA'}", number_format)
        #     row+=1
            
        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'sales_report_from_{self.start_date}_to_{self.end_date}.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'commission.sale.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self'
        }
