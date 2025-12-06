from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    filter_product_tmpl_ids = fields.Many2many('product.template', string='Products',
                                               compute='_compute_filter_product_ids')
    filter_product_ids = fields.Many2many('product.product', string='Products',
                                               compute='_compute_filter_product_ids')


    @api.depends('team_id')
    def _compute_filter_product_ids(self):
        for order in self:
            if self.env.user.has_group('sales_team.group_sale_manager'):
                order.filter_product_tmpl_ids = self.env['product.template'].search([('sale_ok', '=', True)])
                order.filter_product_ids = self.env['product.product'].search([('sale_ok', '=', True)])
            elif order.team_id.product_category_ids:
                order.filter_product_tmpl_ids = self.env['product.template'].search(
                    [('sale_ok', '=', True), ('categ_id','in', order.team_id.product_category_ids.ids)])
                order.filter_product_ids = self.env['product.product'].search(
                    [('sale_ok', '=', True), ('categ_id', 'in', order.team_id.product_category_ids.ids)])
            else:
                order.filter_product_tmpl_ids = None
                order.filter_product_ids = None