from odoo import api, fields, models, _
class HREmployee(models.Model):
    _inherit = "hr.employee"

    # Determines if the employee can access refund-related buttons in POS
    enable_pos_refund_buttons = fields.Boolean(string="Enable POS Refund Buttons", default=False)
    # Determines if the employee can apply discounts in POS
    enable_pos_discount_buttons = fields.Boolean(string="Enable POS Discount Buttons",default=False)
