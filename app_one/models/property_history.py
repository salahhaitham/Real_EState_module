

from odoo import api, fields, models



class Property_history(models.Model):
    _name = 'property.history'


    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state=fields.Char()
    new_state=fields.Char()
    reason=fields.Char()
    property_Lines_ids=fields.One2many('property.history.lines','history_id',)


class Property_history_Lines(models.Model):
    _name='property.history.lines'
    history_id=fields.Many2one('property.history')
    description=fields.Text()
    area=fields.Integer()
