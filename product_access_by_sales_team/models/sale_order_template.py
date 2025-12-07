from odoo import api, fields, models, _

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    team_id = fields.Many2one('crm.team',string='Sales Team', required=True)
    filter_product_ids = fields.Many2many('product.product', string='Products',
                                          compute='_compute_filter_product_ids')

    @api.model
    def default_get(self, default_fields):
        res = super(SaleOrderTemplate, self).default_get(default_fields)
        teams = self.env['crm.team'].search([
            ('company_id', 'in', (False, self.env.company.id)),
            '|', ('user_id', '=', self.env.user.id), ('member_ids', 'in', [self.env.user.id])
        ])
        if teams:
            res.update({'team_id': teams[0].id})
        return res

    @api.depends('team_id')
    def _compute_filter_product_ids(self):
        for template in self:
            if template.team_id and template.team_id.product_category_ids:
                template.filter_product_ids = self.env['product.product'].search(
                    [('sale_ok', '=', True), ('categ_id', 'in', template.team_id.product_category_ids.ids)])
            else:
                template.filter_product_ids = None