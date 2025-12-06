from odoo import _, _lt, api, fields, models

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    @api.readonly
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        """
            Override of `web_search_read` to restrict product visibility based on Sales Team configuration.

        Purpose
        -------
        This method ensures that salespersons can only view or select products that
        belong to the product categories assigned to their Sales Team(s).

        Models Affected:
            - product.template
            - product.product

        Visibility Rules
        ----------------
        1. If the user is a Sales Manager (group_sale_manager):
            - No restrictions apply.
            - User sees all products.

        2. If the user is a Salesperson or Sales Team Member:
            - Only products whose categories are included in the team's
              `product_category_ids` are visible.

        Logic
        -----
        - Identify Sales Teams where the user is:
            * Team Leader (user_id), or
            * Team Member (member_ids)
        - Collect all product categories assigned to those teams.
        - Add a domain restriction so only products belonging to those categories appear.

        Why This Override is Needed
        ---------------------------
        Without this override, users could still see full product lists when:
            - Searching from product menus
            - Selecting products from sale order lines
            - Using smart buttons or search views

        This method enforces uniform access control across all search endpoints.
            """
        if self._name in ('product.template', 'product.product'):
            teams = self.env['crm.team'].search([
                ('company_id', 'in', (False, self.env.company.id)),
                '|', ('user_id', '=', self.env.user.id), ('member_ids', 'in', [self.env.user.id])
            ])
            if teams and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('categ_id', 'in', teams.mapped('product_category_ids').ids)]
        return super(Base, self).web_search_read(domain, specification, offset, limit, order, count_limit)

    @api.model
    @api.readonly
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False, lazy=True):
        """
        Override of `web_read_group` to apply product category restrictions
        on grouped views (kanban, pivot, search panel, etc.)

        Purpose
        -------
        `read_group` is used by Odoo to generate grouped results.
        Even if `web_search_read` is restricted, grouped views
        may still expose product records unless this override is applied.

        Models Affected:
            - product.template
            - product.product

        Visibility Rules
        ----------------
        - If the user is a Sales Manager:
            * Full access. No filtering applied.

        - If user belongs to any Sales Team:
            * Only products in categories assigned to those teams will appear
              in grouped results.

        Why This Override is Required
        ------------------------------
        Grouped views (pivot, kanban, list grouped by category, etc.)
        bypass normal search_read logic.
        Without this method, users might still see:
            - Product counts belonging to restricted categories
            - Aggregated amounts including unauthorized products

        This keeps all product-related views consistent with access control.

        Logic
        -----
        1. Find all Sales Teams associated with the user.
        2. Extract allowed product categories (product_category_ids).
        3. Append domain restriction so grouping only includes authorized data.
            """
        if self._name in ('product.template', 'product.product'):
            teams = self.env['crm.team'].search([
                ('company_id', 'in', (False, self.env.company.id)),
                '|', ('user_id', '=', self.env.user.id), ('member_ids', 'in', [self.env.user.id])
            ])
            if teams and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('categ_id', 'in', teams.mapped('product_category_ids').ids)]
        return super(Base, self).web_read_group(domain, fields, groupby, limit, offset, orderby, lazy)