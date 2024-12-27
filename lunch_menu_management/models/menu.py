from email.policy import default

from odoo import fields,api,models,_
from odoo.exceptions import ValidationError
from odoo.tools.populate import randint


class Menu(models.Model):
    _name="lunch_menu_management.menu"
    _description = "Menu"
    _rec_name = 'menu_item'

    menu_item = fields.Selection(
        [
            ('pizza', 'Pizza'),
            ('burger', 'Burger'),
            ('salad', 'Salad'),
            ('pasta', 'Pasta'),
            ('rice', 'Rice and Curry'),
        ],
        string='Lunch Menu',
        required=True
    )

    price=fields.Monetary(
        string="Price",
        required=True,
        currency_field="default_currency",
        help="Price of the menu item",
    )

    default_currency=fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id
    )

    color = fields.Integer("Color index", default=2)

    @api.model
    def name_create(self,menu_item):
        record=self.create({
            'menu_item':menu_item,
            'color':randint(0,11)
        })
        return record.id,record.display_name

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError(_("Price must be a non-negative value."))

    @api.constrains('color')
    def _check_color(self):
        for rec in self:
            if rec.color < 0 or rec.color > 12:
                raise ValidationError("Color has to be a integer between 0 and 12")