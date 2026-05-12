
from odoo import fields, models

class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
            ('closed', 'Closed'),
        ]
    )
    reason = fields.Char()
    def Confirm_action(self):
        self.property_id.state=self.state
        self.property_id.change_state('closed',self.state,self.reason)