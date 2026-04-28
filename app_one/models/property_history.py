

from odoo import api, fields, models



class Property_history(models.Model):
    _name = 'property.history'
    _description = 'Property.history'

    property_id = fields.Many2one('property',)
    name = fields.Char()
    user_id =fields.Many2one('res.users')
    old_state = fields.Char()
    new_state = fields.Char()


