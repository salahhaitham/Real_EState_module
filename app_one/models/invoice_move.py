from odoo import models, fields,api


class Account_move(models.Model):
     _inherit = 'account.move'


     def action_confirm(self):
        print("inside action_confirm")
