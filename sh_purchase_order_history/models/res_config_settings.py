# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_purchase_configuration_limit = fields.Integer(
        string="Purchase configuration limit ", default=0)
    enable_purchase_reorder = fields.Boolean("Enable Reorder ")
    purchase_day = fields.Integer(
        string="Last No. of Day's Orders ", default=0)
    purchase_stages = fields.Many2many('purchase.order.stages',string="Stages ")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_purchase_configuration_limit = fields.Integer(
        related='company_id.sh_purchase_configuration_limit', readonly=False
    )
    enable_purchase_reorder = fields.Boolean(
        "Enable Reorder ", related="company_id.enable_purchase_reorder", readonly=False)
    purchase_day = fields.Integer(
        "Last No. of Day's Orders ", related="company_id.purchase_day", readonly=False)
    purchase_stages = fields.Many2many('purchase.order.stages',string="Stages ",related="company_id.purchase_stages", readonly=False)
