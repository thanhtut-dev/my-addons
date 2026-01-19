from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    department_id = fields.Many2one('hr.department', 'Department', check_company=True)
    budget_status = fields.Selection([('zero', 'No Budget Left'), ('exceed', 'Exceed'), ('available', 'Available')],
                                     string='Budget Status', default='')
    department_budget_line = fields.Many2one('purchase.budget.line', index=True,)


    @api.onchange('user_id')
    def onchange_user_id(self):
        """
           Automatically set the department based on the selected user.

           When a user is selected on the purchase order, this method assigns
           the department linked to the user's employee record.
           """
        if self.user_id and self.user_id.employee_id:
            self.department_id = self.user_id.employee_id.department_id

    def _send_budget_approval_activity(self, budget_left):
        """
        Send a budget approval activity to the department manager.

        This method creates a To-Do activity for the department manager
        when the purchase order exceeds or reaches the allocated budget.

        :param budget_left: Remaining budget amount for the department
        :type budget_left: float
        """
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        department = self.department_id
        manager = department.manager_id

        if not manager or not manager.user_id:
            raise ValidationError(_('No manager is assigned to this department.'))

        self.activity_schedule(
            activity_type_id=activity_type.id,
            user_id=manager.user_id.id,
            summary="Purchase Order Budget Approval Required",
            note=f"""
            Purchase Order <b>{self.name}</b> exceeds department budget.<br/>
            <b>Total:</b> {self.amount_total}<br/>
            <b>Remaining Budget:</b> {budget_left}
            """,
        )

    def check_budget_limit(self):
        """
        Validate the purchase order against the department budget.

        This method:
        - Retrieves the active and confirmed budget for the order date
        - Calculates total purchase amounts for the department
        - Updates budget status accordingly
        - Sends approval activity if the budget is exceeded
        """
        budget_list = self.env['purchase.budget'].search([('date_from', '<=', self.date_order),
                                                          ('date_to', '>=', self.date_order),
                                                          ('state', '=', 'confirm'),
                                                          ('company_id', '=', self.company_id.id),])
        budget_line = budget_list.mapped('line_ids').filtered(lambda l: l.department_id == self.department_id)[0]
        if not budget_line:
            raise ValidationError(_('No confirmed budget control is configured for this department.'))
        self.department_budget_line = budget_line
        order_list = self.env['purchase.order'].search([('date_order', '>=', budget_line.purchase_budget_id.date_from),
                                                        ('date_order', '<=', budget_line.purchase_budget_id.date_to),
                                                        ('department_id', '=', self.department_id.id),
                                                        ('state', '=', 'purchase'),])
        total_order_amount = sum(order_list.mapped('amount_total')) if order_list else 0
        if total_order_amount >= budget_line.amount:
            self.budget_status = 'zero'
            self._send_budget_approval_activity(0)
            self.state = 'to approve'
        else:
            total_order_amount += self.amount_total
            if total_order_amount < budget_line.amount:
                self.budget_status = 'available'
            else:
                self.budget_status = 'exceed'
                self._send_budget_approval_activity(budget_line.amount - budget_line.purchase_amount)
                self.state = 'to approve'

    def button_confirm(self):
        """
        Override the standard confirmation to enforce budget control.

        Ensures that:
        - A department is assigned
        - Budget validation is performed before confirmation
        """
        for order in self:
            if order.department_id:
                order.check_budget_limit()
            else:
                raise ValidationError(_('No department is assigned to this order.'))
        return super(PurchaseOrder, self).button_confirm()

    def button_approve(self, force=False):
        """
        Update department budget consumption upon approval.

        Once the purchase order is approved, the purchase amount
        is added to the department's consumed budget.
        """
        res = super(PurchaseOrder, self).button_approve(force)
        if self.department_budget_line:
            old_amt = self.department_budget_line.purchase_amount
            self.department_budget_line.write({'purchase_amount': old_amt + self.amount_total})
        return res

    def _approval_allowed(self):
        """
        Control approval permission based on budget status.

        Purchase orders with available budget can be approved
        without additional approval checks.
        """
        if self.budget_status == 'available':
            return True
        return super(PurchaseOrder, self)._approval_allowed()