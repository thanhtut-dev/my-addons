from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class PurchaseBudget(models.Model):
    _name = "purchase.budget"

    name = fields.Char('Budget Name', required=True)
    date_from = fields.Date('Budget Start Date',required=True)
    date_to = fields.Date('Budget End Date',required=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )
    line_ids = fields.One2many('purchase.budget.line', 'purchase_budget_id', string='Budget Lines', copy=True)
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm')], string='Status', default='draft')

    def action_confirm(self):
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Confirmed purchase budgets cannot be deleted.'))
        return super(PurchaseBudget, self).unlink()

class PurchaseBudgetLine(models.Model):
    _name = "purchase.budget.line"

    name = fields.Char('Budget Line Name', required=True)
    purchase_budget_id = fields.Many2one('purchase.budget', index=True, required=True, ondelete='cascade')
    department_id = fields.Many2one('hr.department', 'Department', check_company=True)
    amount = fields.Float('Budget Amount', required=True)
    purchase_amount = fields.Float('Purchase Amount', readonly=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )