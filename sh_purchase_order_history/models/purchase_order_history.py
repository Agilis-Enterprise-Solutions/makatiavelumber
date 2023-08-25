# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class PurchaseOrderStges(models.Model):

    _name = 'purchase.order.stages'
    _description = 'Purchase Order Stages'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(required=True, translate=True, string='Name')
    color = fields.Integer(string='Color', default=1)
    stage_key = fields.Char(required=True, translate=True,
                            string='Stage Keys')

    _sql_constraints = [('name_uniq', 'unique (name)',
                        'Stage name already exists !')]
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, default=lambda self:
                                 self.env.company)


class PurchaseOrderHistory(models.Model):

    _name = 'purchase.order.history'
    _description = 'Purchase Order History'
    _order = "date_order desc"

    purchase_reorder = fields.Boolean('Reorder')
    name = fields.Many2one('purchase.order.line', 'Purchase Order Line')
    order_id = fields.Many2one('purchase.order',
                               'Current Purchase Order', readonly=True)
    status = fields.Selection(string='Status',
                              related='name.order_id.state',
                              readonly=True)
    date_order = fields.Datetime("Date")
    po_id = fields.Char('Purchase Order')
    product_id = fields.Many2one('product.product',
                                 related='name.product_id',
                                 readonly=True)
    price_unit = fields.Float('Price', related='name.price_unit',
                              readonly=True)
    product_qty = fields.Float('Quantity', related='name.product_qty',
                               readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit',
                                  related='name.product_uom',
                                  readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency Id',
                                  related='name.currency_id')
    price_subtotal = fields.Monetary('Subtotal', readonly=True,
                                     related='name.price_subtotal')

    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, default=lambda self:
                                 self.env.company)
    enable_purchase_reorder = fields.Boolean('Enable Reorder Button for Purchase Order History',
                       related='company_id.enable_purchase_reorder')

    # Reorder Button
    def purchases_reorder(self):
        
        vals = {
            'price_unit': self.price_unit,
            'product_qty': self.product_qty,
            'price_subtotal': self.price_subtotal,
            'date_planned': fields.Datetime.now(),
        }

        if self.product_id:
            vals.update({'name': self.product_id.display_name,
                        'product_id': self.product_id.id})

        if self.product_uom:
            vals.update({'product_uom': self.product_uom.id})

        context = self._context.get('params')
        
        if self.order_id:
            vals.update({'order_id': context.get('id')})

        po = self.env['purchase.order'].sudo().browse(context.get('id'))
        po.write({'order_line': [(0, 0, vals)]})
        po._cr.commit()

        return {'type': 'ir.actions.client', 'tag': 'reload'}


    # View Purchase Order Button

    def view_purchase_reorder(self):

        return {
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.name.order_id.id,
        }


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    order_history_line = fields.One2many('purchase.order.history',
                                         'order_id', string='Order History',
                                         compute='_compute_purchase_order_history')
    
    enable_purchase_reorder = fields.Boolean(
        'Enable Reorder Button for Purchase Order History', related='company_id.enable_purchase_reorder')

    # All Lines Reorder Button

    def action_all_purchase_reorder(self):
        for rec in self.order_history_line:
            if self.enable_purchase_reorder:
                vals = {
                    'price_unit': rec.price_unit,
                    'product_qty': rec.product_qty,
                    'price_subtotal': rec.price_subtotal,
                    'date_planned': fields.Datetime.now(),
                }
                if rec.product_id:
                    vals.update({'name': rec.product_id.display_name,
                                'product_id': rec.product_id.id})

                if rec.product_uom:
                    vals.update({'product_uom': rec.product_uom.id})

                if rec.order_id:
                    vals.update({'order_id': self.id})

                self.write({'order_line': [(0, 0, vals)]})
                self._cr.commit()

        return {'type': 'ir.actions.client', 'tag': 'reload'}
    

    @api.model
    @api.onchange('partner_id')
    def _onchange_partner(self):

        self.order_history_line = None
        if self.partner_id:
            partners = []
            domain = []

            partners.append(self.partner_id.id)

            if self.env.company.purchase_day:
                purchase_day = self.env.company.purchase_day
                Display_date = datetime.today() \
                    - relativedelta(days=purchase_day)
                domain.append(('date_order', '>=', Display_date))

            stages = []

            if self.env.company.purchase_stages:
                for stage in self.env.company.purchase_stages:
                    if stage.stage_key:
                        stages.append(stage.stage_key)
                domain.append(('state', 'in', stages))

            if self.env.user.company_id.sh_purchase_configuration_limit:
                limit = self.env.user.company_id.sh_purchase_configuration_limit
            else:
                limit = None

            if self.partner_id.child_ids:
                for child in self.partner_id.child_ids:
                    partners.append(child.id)

            if self._origin:
                domain.append(("id", "!=", self._origin.id))

            if partners:
                domain.append(('partner_id', 'in', partners))

            purchase_order_search = self.env['purchase.order'
                                             ].search(domain, limit=limit,
                                                      order='date_order desc')
            purchase_ordr_line = []
            if purchase_order_search:
                for record in purchase_order_search:

                    if record.order_line:
                        for rec in record.order_line:

                            purchase_ordr_line.append((0, 0, {
                                # 'order_id':record.id,
                                'po_id': record.name,
                                'name': rec.id,
                                'product_id': rec.product_id,
                                'price_unit': rec.price_unit,
                                'date_order': rec.date_order,
                                'product_qty': rec.product_qty,
                                'product_uom': rec.product_uom,
                                'price_subtotal': rec.price_subtotal,
                                'status': rec.state,
                            }))
                            
                            print("\n\n\n\n\n\n purchase_ordr_line.....", purchase_ordr_line)
                self.order_history_line = purchase_ordr_line

    def _compute_purchase_order_history(self):
        for vals in self:
            vals.order_history_line = None

            if vals.partner_id:
                partners = []
                domain = []

                partners.append(vals.partner_id.id)

                history_domain = [] 
                if self.env.company.purchase_day:
                    purchase_day = self.env.company.purchase_day
                    Display_date = datetime.today() \
                        - relativedelta(days=purchase_day)
                    domain.append(('date_order', '>=', Display_date))
                    history_domain.append(("date_order", ">=", Display_date),)

                stages = []

                if self.env.company.purchase_stages:
                    for stage in self.env.company.purchase_stages:
                        if stage.stage_key:
                            stages.append(stage.stage_key)
                    domain.append(('state', 'in', stages))
                    history_domain.append(("status", "in", stages),)

                if self.env.user.company_id.sh_purchase_configuration_limit:
                    limit = self.env.user.company_id.sh_purchase_configuration_limit
                else:
                    limit = None

                if vals.partner_id.child_ids:
                    for child in vals.partner_id.child_ids:
                        partners.append(child.id)

                if partners:
                    domain.append(('partner_id', 'in', partners))
                    history_domain.append(('order_id.partner_id','in',partners),)

                if vals.id:
                    domain.append(("id", "!=", vals.id))
                
                purchase_order_search = self.env['purchase.order'
                                                ].search(domain, limit=limit,
                                                        order='date_order desc')
                
        
                history_domain.append(('order_id','in',purchase_order_search.ids),)
        
                if purchase_order_search:
                    for record in purchase_order_search:
                        history_ids = self.env['purchase.order.history'].sudo().search(
                                                            history_domain,
                                                            limit=limit,
                                                            order="date_order desc",
                                                        )
                        if record.order_line:
                            for rec in record.order_line:
                                if rec.id in history_ids.name.ids:
                                    vals.order_history_line = [(6, 0, history_ids.ids)]
                                else:
                                    history_vals = {
                                        'order_id':record.id,
                                        'po_id': record.name,
                                        'name': rec.id,
                                        'product_id': rec.product_id,
                                        'price_unit': rec.price_unit,
                                        'date_order': rec.date_order,
                                        'product_qty': rec.product_qty,
                                        'product_uom': rec.product_uom,
                                        'price_subtotal': rec.price_subtotal,
                                        'status': rec.state,
                                    }
                                    res = self.env['purchase.order.history'].sudo().create(history_vals)