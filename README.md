# my-addons
This repository contains custom Odoo modules designed and developed by myself.
Each module is built to improve business workflows, enhance usability, and extend
the native Odoo functionality. These addons reflect my real-world development
experience across Odoo 16–19 (Community & Enterprise).

## Available Modules

### 1. product_uom_relative_filter
- Smart UoM Domain Filter — On transaction forms (SO, PO, stock moves, invoices), the UoM dropdown only shows units related to the product's UoM via relative_uom_id chain.
- Bidirectional Chain Traversal — Walks both up and down the relative_uom_id chain (e.g., MG ↔ G ↔ KG ↔ Ton).
- Product Form UoM Filter — Also filters Purchase UoM on product form to only show compatible units.

