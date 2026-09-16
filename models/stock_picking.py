# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_notes = fields.Text(
        string='Delivery Notes',
        help='Delivery notes from the related sale order'
    )
