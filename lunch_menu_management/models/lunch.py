from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Lunch(models.Model):
    _name = 'lunch_menu_management.lunch'
    _description = 'Lunch Order'

    name = fields.Char(string="User Name", required=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    menu_item_ids = fields.Many2many(
        'lunch_menu_management.menu',
        'lunch_menu_rels',
        'lunch_id',
        'menu_id'
    )

    day = fields.Char(string="Day", compute="_compute_day", store=True)
    @api.depends('date')
    def _compute_day(self):
        for record in self:
            if record.date:
                record.day = record.date.strftime('%A')


    qty = fields.Integer(string="Quantity", required=True)
    total_price = fields.Float(string="Total Bill", compute="_computed_total_price")

    @api.depends('menu_item_ids', 'qty')
    def _computed_total_price(self):
        for record in self:
            total= sum(menu.price for menu in record.menu_item_ids)
            record.total_price=total * record.qty

    @api.constrains('qty')
    def _check_quantity(self):
        for record in self:
            if record.qty <= 0:
                raise ValidationError(_("Quantity must be greater than 0."))

    @api.ondelete(at_uninstall=False)
    def _on_delete_cleanup(self):
        for record in self:
            if record.date and record.date < fields.Date.today():
                raise UserError(_("You cannot delete past lunch menu records."))

    # @api.onchange('menu_item')
    # def _onchange_menu_item(self):
    #     if self.menu_item:
    #         if self.menu_item == 'pizza':
    #             self.price = 12.00
    #         elif self.menu_item == 'burger':
    #             self.price = 8.00
    #         elif self.menu_item == 'salad':
    #             self.price = 6.00
    #         elif self.menu_item == 'pasta':
    #             self.price = 10.00
    #         elif self.menu_item == 'rice':
    #             self.price = 9.00
    #
    #         return {
    #             'warning': {
    #                 'title': _("Price Updated"),
    #                 'message': _(f"The price has been updated based on the selected menu item \"{self.menu_item}\" and the price is \"{self.price}\".")
    #             }
    #         }


    def write(self, vals):
        for record in self:
            if 'qty' in vals and vals['qty'] <= 0:
                raise ValidationError(_("Quantity must be greater than 0."))

            if 'date' in vals and vals['date'] < fields.Date.today().isoformat():
                raise UserError(_("You cannot modify records for past dates."))
        return super().write(vals)



