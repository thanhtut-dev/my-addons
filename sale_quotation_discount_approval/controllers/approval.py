from odoo import http
from odoo.http import request
from odoo import _

class DiscountApprovalController(http.Controller):

    @http.route('/sale/discount/approval', type='http', auth='public', csrf=False)
    def approve_discount(self, order_id=None, decision=None, **kwargs):
        order = request.env['sale.order'].sudo().browse(int(order_id))

        if not order.exists():
            return "Invalid order."

        if order.sudo().approval_state in ('approved', 'rejected'):
            return "Order already approved or rejected.No action required for this order."

        if decision == 'approve':
            order.sudo().write({'approval_state': 'approved'})
            order.sudo().message_post(body=_("Order approved by %s") % order.team_id.user_id.name, email_from = order.team_id.user_id.email)
            return "Sale order approved successfully. You may close this window."

        if decision == 'reject':
            order.sudo().write({'approval_state': 'rejected'})
            order.sudo().message_post(body=_("Order rejected by %s") % order.team_id.user_id.name, email_from = order.team_id.user_id.email)
            return "Sale order rejected. You may close this window."

        return "Invalid decision."
