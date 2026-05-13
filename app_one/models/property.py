from psycopg2._psycopg import Boolean
from typing_extensions import ReadOnly

from odoo import api, fields, models
from odoo.cli.scaffold import env
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name='property'
    _description = 'Property1'
    _inherit = ['mail.thread','mail.activity.mixin']

    name=fields.Char(size=2)
    ref=fields.Char(default='New',readonly=1)
    post_code = fields.Char(required=True)
    livig_area = fields.Integer(required=True)
    faceds = fields.Integer()
    description = fields.Text()
    date_available = fields.Date(tracking=True)
    expected_selling_date = fields.Date()
    is_late = fields.Boolean()
    expected_price=fields.Float(digits=(0,2))
    selleing_price=fields.Float()
    bedrooms=fields.Integer()
    bathrooms=fields.Integer()
    diff=fields.Float(compute='_compute_diff')
    garage=fields.Boolean()
    garden=fields.Boolean()
    active=fields.Boolean(default=True)
    state=fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
            ('closed', 'Closed'),
        ],default='draft'
    )
    garden_orientation= fields.Selection(
       [
           ('south','South'),
           ('north','North'),
           ('west', 'West'),
           ('east', 'East'),

        ],default='south'
    )
    owner_id=fields.Many2one('owner')
    owner_phone=fields.Char(related='owner_id.phone')
    owner_address= fields.Char(related='owner_id.address')
    tag_ids=fields.Many2many('tag',)
    property_lines_id=fields.One2many('property.lines', 'property_id')


    def change_state(self,old_state,new_state,reason =""):
        for rec in self:
         rec.env['property.history'].create({
           'user_id':self.env.uid,
           'old_state':old_state,
           'new_state':new_state,
           'property_id':self.id,
             'reason':reason or "",
             'property_Lines_ids':[(0,0,{'description':line.description,'area':line.area})for line in rec.property_lines_id]
         }  )



    def change_state_action(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'app_one.change_state_action_id'
        )

        action['context'] = {
            'default_property_id': self.id
        }

        return action




    _sql_constraints = [('unique_name','unique (name)','name is unique')]


    def check_expected_sellingDate(self):
       property_ids=self.search([])
       for record in property_ids:
            if record.expected_selling_date and record.expected_selling_date<fields.Datetime.today():
                     record.is_late=True

            


    @api.constrains('livig_area')
    def _check_livig_area(self):
        for record in self:
            if record.livig_area==0:
                raise ValidationError("Living Area cannot be 0")
            
    @api.onchange('selleing_price')       
    def _onchange_selleing_price(self):
        for record in self:
            if record.selleing_price<0:
               return {
                'warning':{'title':'warning','message':'assign negative value' ,'type':'notification'},
                }


    def create(self,vals_list):
        res=super().create(vals_list)
        if res.ref=="New":
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        return  res



    @api.model
    def web_search_read(self, *args, **kwargs):
        print("SEARCH")
        return super().web_search_read(*args, **kwargs)

    def unlink(self) :
        print("delete method")
        return super().unlink()
    def write(self, vals):
        res = super(Property, self).write(vals)
        print("writeee method")
        return res
    @api.depends('expected_price','selleing_price')
    def _compute_diff(self):
        for record in self:
            record.diff=record.expected_price-record.selleing_price


    def draft_button(self):
        self.change_state(self.state, 'draft')
        self.write({'state': 'draft'})

    def pending_button(self):
        self.change_state(self.state, 'pending')
        self.write({'state': 'pending'})

    def sold_button(self):
        self.change_state(self.state, 'sold')
        self.write({'state': 'sold'})

    def close_button(self):
        self.change_state(self.state, 'closed')
        for rec in self:
            rec.state='closed'




class Property_Lines(models.Model):
    _name='property.lines'
    property_id=fields.Many2one('property')
    description=fields.Text()
    area=fields.Integer()
