from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CrmTeam(models.Model):
    _inherit = "crm.team"

    discount_limit = fields.Float(string="Discount Limit %", required=True)

    @api.constrains('discount_limit')
    def _check_discount_limit(self):
        for team in self:
            if not team.discount_limit:
                raise ValidationError("Discount Limit % is required.")