from odoo import api, fields, models, _
class HREmployee(models.Model):
    _inherit = "hr.employee"

    # Determines if the employee can access refund-related buttons in POS
    enable_pos_refund_buttons = fields.Boolean(string="Enable POS Refund Buttons", default=False)
    # Determines if the employee can apply discounts in POS
    enable_pos_discount_buttons = fields.Boolean(string="Enable POS Discount Buttons",default=False)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
            Extend POS employee data loading.

            This method adds custom permission fields to the list of
            employee fields sent to the POS frontend, making them
            available for JavaScript / OWL logic.
            """
        result = super(HREmployee, self)._load_pos_data_fields(config_id)
        result += ['enable_pos_refund_buttons','enable_pos_discount_buttons']
        return result