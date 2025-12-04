from odoo import _, _lt, api, fields, models

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    @api.readonly
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        """
            Override of web_search_read to apply Sales Team–based record visibility rules.

            This method restricts which records a salesperson can see in:
                - Customer list (res.partner)
                - Sale Orders (sale.order)
                - CRM Leads / Opportunities (crm.lead)

            The restriction does NOT apply to:
                - Sales Managers (group_sale_manager)
                - Internal users without sales access logic

            Visibility Rules Implemented:
            ----------------------------------

            1. res.partner (Customers)
               - Only applied when Odoo is searching for customers
                 (context: res_partner_search_mode='customer')
               - Salespersons can see ONLY customers assigned to their Sales Teams.
               - Sales Managers can see all customers.

            2. sale.order (Quotations / Sales Orders)
               - Salespersons only see Sale Orders belonging to their Sales Teams.
               - Sales Managers can see all Sale Orders.

            3. crm.lead (Leads / Opportunities)
               - Salespersons only see Leads assigned to their Sales Teams.
               - Sales Managers can see all Leads.

            Technical Flow:
            ----------------------------------
            - Identify all Sales Teams where the user is:
                * team leader (user_id)
                * team member (member_ids)
            - Use these teams to filter domain results:
                * For customers: partner_ids of those teams
                * For leads & orders: team_id of those teams

            This ensures complete team-based data isolation for salespersons.
            """

        if self._name in ('res.partner', 'sale.order', 'crm.lead'):
            teams = self.env['crm.team'].search([
                ('company_id', 'in', (False, self.env.company.id)),
                '|', ('user_id', '=', self.env.user.id), ('member_ids', 'in', [self.env.user.id])
            ])
            #1. Customer List
            if self._name == 'res.partner' and self.env.context.get('res_partner_search_mode') == 'customer' and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('id', 'in', teams.partner_ids.ids)]
            #2. Sale List
            if self._name == 'sale.order'and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('team_id', 'in', teams.ids)]
            #3. CRM Lead/opportunity list
            if self._name == 'crm.lead' and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('team_id', 'in', teams.ids)]
        return super(Base, self).web_search_read(domain, specification, offset, limit, order, count_limit)

    @api.model
    @api.readonly
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False, lazy=True):
        """
            Override of web_read_group to apply Sales Team–based grouping restrictions.

            Purpose:
            ----------------------------------
            This method ensures that grouped results (kanban, pivot, graph, search panel)
            follow the same visibility restrictions as web_search_read.

            Why needed:
            ----------------------------------
            Even if search_read is restricted, a user may still see unauthorized data
            through:
                - Grouped kanban view
                - Pivot table
                - Graph view
                - Search panel filters
            Therefore, read_group must also apply the same team-based rules.

            Visibility Rules:
            ----------------------------------

            1. res.partner (Customers)
               - Only show customers assigned to the user's Sales Teams
               - Sales Managers see all customers
               - Restriction applies only when searching for customers
                 (res_partner_search_mode='customer')

            2. sale.order
               - Only show Sale Orders belonging to the user's Sales Teams

            3. crm.lead (if included in future)
               - Only show Leads belonging to the user's Sales Teams

            Technical Flow:
            ----------------------------------
            - Determine all Sales Teams the user belongs to.
            - Append domain conditions that restrict group results:
                * For customers: ('id', 'in', team.customer_ids)
                * For orders/leads: ('team_id', 'in', team_ids)
            """
        if self._name in ('res.partner', 'sale.order'):
            teams = self.env['crm.team'].search([
                ('company_id', 'in', (False, self.env.company.id)),
                '|', ('user_id', '=', self.env.user.id), ('member_ids', 'in', [self.env.user.id])
            ])
            # 1. Customer List
            if self._name == 'res.partner' and self.env.context.get(
                    'res_partner_search_mode') == 'customer' and not self.env.user.has_group(
                    'sales_team.group_sale_manager'):
                domain += [('id', 'in', teams.partner_ids.ids)]
            # 2. Sale List
            if self._name == 'sale.order' and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('team_id', 'in', teams.ids)]
            # 3. CRM Lead/opportunity list
            if self._name == 'crm.lead' and not self.env.user.has_group('sales_team.group_sale_manager'):
                domain += [('team_id', 'in', teams.ids)]
        return super(Base, self).web_read_group(domain, fields, groupby, limit, offset, orderby, lazy)