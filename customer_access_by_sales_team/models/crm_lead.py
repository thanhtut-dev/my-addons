from odoo import api, fields, models, _
class CrmLead(models.Model):
    _inherit = "crm.lead"

    partner_ids = fields.Many2many('res.partner', string='Customers list by sales team', compute='_compute_partner_ids')

    @api.depends('user_id')
    def _compute_partner_ids(self):
        for lead in self:
            if self.env.user.has_group('sales_team.group_sale_manager'):
                lead.partner_ids = self.env['res.partner'].search([('customer_rank', '>', 0)])
            else:
                teams = self.env['crm.team'].search([
                    ('company_id', 'in', (False, self.env.company.id)),
                    '|', ('user_id', '=', lead.user_id.id), ('member_ids', 'in', [lead.user_id.id])
                ])
                lead.partner_ids = teams.partner_ids