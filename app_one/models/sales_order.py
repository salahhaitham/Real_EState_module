from odoo import models, fields,api


class Sales_order(models.Model):
     _inherit = 'sale.order'
     property_id=fields.Many2one('property')
     price= fields.Float(compute='_compute_price', store=True)

     def action_confirm(self):
         rec=super().action_confirm()
         print("inside action_confirm")
         return rec

     @api.depends('property_id', 'property_id.selleing_price')
     def _compute_price(self):
         for record in self:
             record.price = record.property_id.selleing_price or 0.0
