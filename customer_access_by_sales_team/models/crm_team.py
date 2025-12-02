from odoo import api, fields, models, _

class CrmTeam(models.Model):
    _inherit = "crm.team"

    partner_ids = fields.Many2many('res.partner',string="Customers", domain="[('customer_rank', '>', 0)]")