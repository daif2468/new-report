# -*- coding: utf-8 -*-
from odoo import models, fields, api


NON_PRODUCT_DISPLAY_TYPES = {
    'line_section',
    'line_note',
    'payment_term',
    'tax',
    'rounding',
    'epd',
}


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Delivery Notes
    delivery_notes = fields.Text(
        string='Delivery Notes',
        help='Delivery notes copied from the related sale order',
        copy=False,
    )

    # Discount Amounts
    amount_before_discount = fields.Monetary(
        string="Total Before Discount",
        compute='_compute_discount_amounts',
        store=True,
        currency_field='currency_id',
    )

    amount_discount = fields.Monetary(
        string="Discount Amount",
        compute='_compute_discount_amounts',
        store=True,
        currency_field='currency_id',
    )

    @api.depends(
        'invoice_line_ids.price_unit',
        'invoice_line_ids.quantity',
        'invoice_line_ids.discount',
        'invoice_line_ids.display_type',
        'invoice_line_ids.price_total',
        'amount_total',
    )
    def _compute_discount_amounts(self):
        for move in self:
            total_before = 0.0

            for line in move.invoice_line_ids:
                # تجاهل السطور غير الخاصة بالمنتجات
                if line.display_type in NON_PRODUCT_DISPLAY_TYPES:
                    continue

                # تجاهل سطور الخصم العام / القيم السالبة
                if line.price_unit < 0:
                    continue

                # حساب الإجمالي قبل الخصم
                if line.discount and line.discount < 100:
                    total_before += line.price_total / (
                        1 - line.discount / 100.0
                    )
                else:
                    total_before += line.price_total

            move.amount_before_discount = total_before
            move.amount_discount = total_before - move.amount_total
