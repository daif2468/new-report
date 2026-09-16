# -*- coding: utf-8 -*-
{
    'name': 'New Reports',
    'version': '18.0.1.0.0',
    'summary': 'Custom reports for sale orders',
    'category': 'Reporting',
    'author': 'Daif',
    'description': """
        This module provides custom reports for sale orders and stock picking:
        - Sale order report with internal reference instead of tax column
        - Sale order report with barcode instead of tax column
        - Stock picking report with product description
    """,
    'depends': [
        'sale',
        'account',
        'stock',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_view.xml',
        'report/paperformat.xml',
        'report/report_invoice_internal_ref.xml',
        'report/report_saleorder_barcode.xml',
        'report/report_saleorder_delivery.xml',
        'report/report_saleorder_internal_ref.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'new_reports/static/src/css/report_fonts.css',
        ],
        'web.report_assets_common': [
            'new_reports/static/src/css/report_fonts.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
