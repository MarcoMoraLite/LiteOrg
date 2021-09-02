# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import tools

class SaleReport(models.Model):
    _name = "valida_curp.report"
    _description = "Panel informativo"
    _auto = False

    #@api.model
    #def _get_done_states(self):
    
    ine_count = fields.Integer('Conteno INE', readonly=True)
    ced_count = fields.Integer('Conteno cédula', readonly=True)
    selfie_count = fields.Integer('Conteno Selfie', readonly=True)
    primerApellido = fields.Char('Primer apellido', readonly=True)
    curp = fields.Char('Curp', readonly=True)
    
    #happy_count = fields.Integer('Conteno registro exitoso', readonly=True)
    #fd_count = fields.Integer('Conteno registros incompletos', readonly=True)

    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        
        select_ = """
            vc.id as id,
            count((CASE vc.state WHEN 'ine' THEN 0 ELSE 1.0 END)) as ine_count,
            count((CASE vc.state WHEN 'cedula' THEN 1.0 ELSE 0 END)) as ced_count,
            count((CASE vc.state WHEN 'foto' THEN 1.0 ELSE 0 END)) as selfie_count,
            vc.curp as curp
        """
        for field in fields.values():
            select_ += field
        
        from_ = """
                valida_curp_valida_curp vc
                %s
        """ % from_clause

        
        groupby_ = """
            vc.state,
            vc.curp,
            vc.id %s
        """ % (groupby)
        
        return '%s (SELECT %s FROM %s WHERE vc.state IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)
    
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))