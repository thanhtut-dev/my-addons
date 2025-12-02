from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_ids = fields.Many2many('res.partner', string='Customers list by sales team', related="team_id.partner_ids")