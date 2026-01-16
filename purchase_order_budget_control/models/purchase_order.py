from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    department_id = fields.Many2one('hr.department', 'Department', check_company=True)
    budget_status = fields.Selection([('zero', 'No Budget Left'), ('exceed', 'Exceed'), ('available', 'Available')],
                                     string='Budget Status', default='')


    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id and self.user_id.employee_id:
            self.department_id = self.user_id.employee_id.department_id

    def check_budget_limit(self):
        budget_list = self.env['purchase.budget'].search([('date_from', '<=', self.date_order),
                                                          ('date_to', '>=', self.date_order),
                                                          ('state', '=', 'confirm'),
                                                          ('company_id', '=', self.company_id.id),])
        budget_line = budget_list.mapped('line_ids').filtered(lambda l: l.department_id == self.department_id)
        if not budget_line:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Budget Information',
                    'message': 'No budget limit setup for this department.',
                    'type': 'info',
                    'sticky': False,
                }
            }
        order_list = self.env['purchase.order'].search([('date_order', '>=', budget_line.purchase_budget_id.date_from),
                                                        ('date_order', '<=', budget_line.purchase_budget_id.date_to),
                                                        ('department_id', '=', self.department_id.id),
                                                        ('state', '=', 'purchase'),])
        total_order_amount = sum(order_list.mapped('amount_total')) if order_list else 0
        if total_order_amount >= budget_line.amount:
            return 'zero'
        total_order_amount += self.amount_total
        if total_order_amount < budget_line.amount:
            budget_line.write({'purchase_amount': total_order_amount})
            return 'available'
        else:
            return 'exceed'


    def budget_control_action(self):
        result = self.check_budget_limit()
        if result == 'zero':
            self.budget_status = 'zero'
            raise ValidationError(_('Department does not have any budget left for this order.'))
        elif result == 'exceed':
            self.budget_status = 'exceed'
            raise ValidationError(_('Current order amount exceed the budget left for its department.'))
        elif result == 'available':
            self.budget_status = 'available'


    def button_confirm(self):
        for order in self:
            if self.department_id:
                if order.budget_status != 'available':
                    order.budget_control_action()
            else:
                raise ValidationError(_('There is no department with this order.'))
        return super(PurchaseOrder, self).button_confirm()