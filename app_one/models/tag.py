
from odoo import models,fields



class Tag(models.Model):
    _name='tag'
    property_ids=fields.Many2many('property')


    name=fields.Char(size=20)






