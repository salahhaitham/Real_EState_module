from odoo import   fields,models



class changeStateWizard(models.TransientModel):
    _name = 'change.state'


    property_id=fields.Many2one('property')
    reason=fields.Char()
    state=fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),

        ]
    )

    def confirm_button(self):
    
           self.property_id.state=self.state
           self.property_id.change_state('closed',self.state)