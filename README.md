# my-addons
This repository contains custom Odoo modules designed and developed by myself.
Each module is built to improve business workflows, enhance usability, and extend
the native Odoo functionality. These addons reflect my real-world development
experience across Odoo 16–18 (Community & Enterprise).

## Available Modules

### 1. sale_discount_approval
- Adds approval workflow for discounts in Sales Order.
- Team leader approval required based on whether total discount is exceed discount limit defined in sales team or not.

## 2. customer_access_by_sales_team
- Separate access rights for Team Leaders and Team Members.
- Administrators can assign customers to Sales Teams. Only Sales Administrators can see all customers.
- Team Leaders and Members can only select customers related to their Sales Team in Sales, CRM Leads, and Opportunities.
- Team Leaders and Members can view only Sale Orders, Leads, and Opportunities created by their own team.

## 3. product_access_by_sales_team
- Restrict product visibility based on Sales Team configuration.
- Sales Administrators can access all products and manage product category assignments in each Sales Team.
- Each Sales Team can only see Quotation Templates assigned to that team.

## 4. pos_control_buttons_access
- Employee-level POS access control.
- Refund and discount button restriction.
- Simple and user-friendly configuration.
- Improved POS security and control.

## 5. purchase_order_budget_control
- Department-based purchase budget configuration.
- Budget period control with start and end dates.
- Automatic validation of Purchase Orders against confirmed budgets.
- Real-time tracking of purchase amount consumption.
- Automatic approval enforcement when budget limits are exceeded.
- Activity notification sent to department managers for approval.
- Seamless integration with the standard Purchase workflow.
- Multi-company support.
- Fully compatible with Odoo (v16, v17, v18).