# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleReport(models.Model):
    _name = "valida_curp.report"
    _description = "Panel informativo"

    @api.model
    def _get_done_states(self):

    ine_count = fields.Integer('Conteno INE', readonly=True)
    ced_count = fields.Integer('Conteno cédula', readonly=True)
    selfie_count = fields.Integer('Conteno Selfie', readonly=True)
    #happy_count = fields.Integer('Conteno registro exitoso', readonly=True)
    #fd_count = fields.Integer('Conteno registros incompletos', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause='valida_curp_valida_curp'):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            count((CASE vc.state WHEN 'ine' THEN 1.0 ELSE 0 END)) as ine_count
            count((CASE vc.state WHEN 'cedula' THEN 1.0 ELSE 0 END)) as ced_count
            count((CASE vc.state WHEN 'foto' THEN 1.0 ELSE 0 END)) as selfie_count
                
        """

        for field in fields.values():
            select_ += field

        from_ = """
                valida_curp_valida_curp vc
                %s
        """ % from_clause

        groupby_ = """
            vc.state %s
        """ % (groupby)

        return '%s (SELECT %s FROM %s WHERE vc.state IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)