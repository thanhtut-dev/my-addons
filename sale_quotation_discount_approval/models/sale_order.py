from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from werkzeug.urls import url_encode

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('draft','Draft'),
        ('waiting','Waiting for Approval'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ], string='Approval Status', default='draft', copy=False, store=True)
    approval_requested_by = fields.Many2one('res.users', string='Requested By', copy=False)
    discount_percent = fields.Float(string='Order Discount (%)', compute='_compute_discount_percent', store=True, digits=(16,2))

    @api.depends('order_line.price_unit', 'order_line.discount', 'order_line.product_uom_qty')
    def _compute_discount_percent(self):
        for order in self:
            total_before = 0.0
            total_after = 0.0
            for line in order.order_line:
                qty = line.product_uom_qty or 0.0
                if line.product_packaging_id and line.product_packaging_qty > 0:
                    qty = line.product_packaging_qty
                price = line.price_unit or 0.0
                disc = line.discount or 0.0
                line_total_before = price * qty
                line_total_after = price * qty * (1 - (disc / 100.0))
                total_before += line_total_before
                total_after += line_total_after
            if total_before > 0:
                # effective discount percent across order
                order.discount_percent = (1 - (total_after / total_before)) * 100
            else:
                order.discount_percent = 0.0

    def action_request_approval(self, reason=None):
        self.ensure_one()
        if self.discount_percent <= self.team_id.discount_limit:
            raise UserError(_("No approval required for this quotation. Overall discount is less than or equal to discount limit defined in sales team."))
        # mark who requested
        self.write({
            'approval_state': 'waiting',
            'approval_requested_by': self.env.user.id,
        })
        # create activity / chatter
        if not self.team_id:
            raise ValidationError(_('There is no sales team in your quotation.'))
        if not self.team_id.user_id:
            raise ValidationError(_(f'There is no team leader in sales team {self.team_id.name}.'))
        approver = self.team_id.user_id
        if approver:
            self.send_approval_request_email()
            # post message
            self.sudo().message_post(body=_(f"Approval requested. Notified approver: {approver.name}"))
        else:
            self.sudo().message_post(body=_("Approval requested, but no approvers found. Check rule configuration."))

    def send_approval_request_email(self):
        template = self.env.ref('sale_quotation_discount_approval.mail_template_discount_approval')
        template.send_mail(self.id, force_send=True)

    def _build_approval_url(self, decision):
        base_url = self.get_base_url()
        params = {
            'order_id': self.id,
            'decision': decision
        }
        return f"{base_url}/sale/discount/approval?{url_encode(params)}"


    def action_approve(self):
        self.ensure_one()
        # permission check: must be team leader of sales team that belongs to order
        if not (self.env.user == self.team_id.user_id):
            raise UserError(_("You are not allowed to approve order from different sales team."))
        self.write({'approval_state': 'approved'})
        self.sudo().message_post(body=_("Order approved by %s") % self.env.user.name)

    def action_reject(self):
        self.ensure_one()
        # permission check: must be team leader of sales team that belongs to order
        if not (self.env.user == self.team_id.user_id):
            raise UserError(_("You are not allowed to reject order from different sales team."))
        self.write({'approval_state': 'rejected'})
        # revert to draft so salesperson can modify
        self.write({'state':'draft'})
        self.sudo().message_post(body=_("Order rejected by %s.") % self.env.user.name)

    def action_confirm(self):
        for order in self:
            if not order.team_id:
                raise ValidationError(_("There is no sales team in your quotation."))

            if not order.team_id.discount_limit:
                raise ValidationError(_(f"There is no discount limit define in sales team '{order.team_id.name}'."))

            if self.env.user != order.team_id.user_id and order.discount_percent > order.team_id.discount_limit and order.approval_state != 'approved':
                if order.approval_state == 'draft':
                    raise UserError(_("This order requires approval for the discount (current: %s%%). Request approval first.") % round(order.discount_percent,2))
                else:
                    raise ValidationError(_("Please wait for approval to confirm the quotation."))
        return super(SaleOrder, self).action_confirm()
