from odoo import api, fields, models, _
class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_hr_employee(self):
        res = super(PosSession, self)._loader_params_hr_employee()
        if res.get('search_params') and res.get('search_params').get('fields'):
            res['search_params']['fields'] += ['enable_pos_refund_buttons','enable_pos_discount_buttons']
        return res