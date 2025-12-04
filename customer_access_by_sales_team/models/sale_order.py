from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_ids = fields.Many2many('res.partner', string='Customers list by sales team', compute='_compute_partner_ids')

    @api.depends('team_id')
    def _compute_partner_ids(self):
        for order in self:
            if self.env.user.has_group('sales_team.group_sale_manager'):
                order.partner_ids = self.env['res.partner'].search([('customer_rank', '>', 0)])
            else:
                order.partner_ids = self.team_id.partner_ids