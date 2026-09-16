from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # =========================================================
    # Delivery Notes
    # =========================================================
    delivery_notes = fields.Text(
        string='Delivery Notes',
        help='Additional notes for delivery',
    )

    # =========================================================
    # Quantity Totals
    # =========================================================
    total_qty_no_discount = fields.Float(
        string='Total Qty (No Discount)',
        compute='_compute_totals_no_discount',
        store=False,
    )

    total_delivered_no_discount = fields.Float(
        string='Total Delivered (No Discount)',
        compute='_compute_totals_no_discount',
        store=False,
    )

    @api.depends(
        'order_line.product_uom_qty',
        'order_line.qty_delivered',
        'order_line.price_unit',
    )
    def _compute_totals_no_discount(self):
        for order in self:
            lines = order.order_line.filtered(
                lambda line: (
                    not line.display_type
                    and line.price_unit >= 0
                )
            )

            order.total_qty_no_discount = sum(
                lines.mapped('product_uom_qty')
            )

            order.total_delivered_no_discount = sum(
                lines.mapped('qty_delivered')
            )

    # =========================================================
    # Discount Amounts
    # =========================================================
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
        'order_line.price_unit',
        'order_line.product_uom_qty',
        'order_line.discount',
        'order_line.display_type',
        'order_line.price_total',
        'amount_total',
    )
    def _compute_discount_amounts(self):
        for order in self:
            total_before = 0.0

            for line in order.order_line:
                # Ignore sections, notes and down payment lines
                if line.display_type or line.is_downpayment:
                    continue

                # Ignore negative price lines
                if line.price_unit < 0:
                    continue

                # Calculate amount before discount
                if line.discount and line.discount < 100:
                    total_before += line.price_total / (
                        1 - line.discount / 100.0
                    )
                else:
                    total_before += line.price_total

            order.amount_before_discount = total_before
            order.amount_discount = (
                total_before - order.amount_total
            )

    # =========================================================
    # Confirm Sale Order
    # =========================================================
    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            if order.delivery_notes:
                for picking in order.picking_ids:
                    picking.delivery_notes = order.delivery_notes

        return res

    # =========================================================
    # Create Invoices
    # =========================================================
    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(
            grouped=grouped,
            final=final,
            date=date,
        )

        for move in moves:
            orders = move.invoice_line_ids.sale_line_ids.order_id

            notes = [
                order.delivery_notes
                for order in orders
                if order.delivery_notes
            ]

            if notes:
                move.delivery_notes = '\n'.join(notes)

        return moves
