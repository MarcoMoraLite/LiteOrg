# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import tools

class SaleReport(models.Model):
    _name = "valida_curp.report"
    _description = "Panel informativo"

    #@api.model
    #def _get_done_states(self):
    
    ine_count = fields.Integer('Conteo INE 1', readonly=True)
    ced_count = fields.Integer('Conteo cédula 1', readonly=True)
    selfie_count = fields.Integer('Conteo foto 1', readonly=True)
    ine_aux = fields.Integer('Conteo INE', readonly=True)
    ced_aux = fields.Integer('Conteo cédula', readonly=True)
    selfie_aux = fields.Integer('Conteo foto', readonly=True)
    curp = fields.Char('Curp', readonly=True)
    state = fields.Char('Estatus', readonly=True)
    nombres = fields.Char('Nombres', readonly=True)
    faltan_datos = fields.Integer('Estatus general 1', readonly=True)
    faltan_datos_aux = fields.Integer('Estatus general', readonly=True)
    total_registros = fields.Integer('Total registros', readonly=True)
    exitoso_registro = fields.Integer('Registros completos 1', readonly=True)
    exitoso_registro_aux = fields.Integer('Registros completos', readonly=True)
    rechazo_registro = fields.Integer('Registros rechazados 1', readonly=True)
    rechazo_registro_aux = fields.Integer('Registros rechazados', readonly=True)
    fecha = fields.Datetime('Fecha de registro',readonly=True)

    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        
        select_ = """
            vc.id as id,
            count((CASE vc.state WHEN 'ine' THEN 1.0 ELSE 0 END)) as ine_count,
            count((CASE vc.state WHEN 'cedula' THEN 1.0 ELSE 0 END)) as ced_count,
            count((CASE vc.state WHEN 'foto' THEN 1.0 ELSE 0 END)) as selfie_count,
            (CASE vc.state WHEN 'ine' THEN 1.0 ELSE 0 END) as ine_aux,
            (CASE vc.state WHEN 'cedula' THEN 1.0 ELSE 0 END) as ced_aux,
            (CASE vc.state WHEN 'foto' THEN 1.0 ELSE 0 END) as selfie_aux,
            vc.curp as curp,
            vc.state as state,
            vc.nombres as nombres,
            count((CASE vc.estatus_gen WHEN 'Faltan datos' THEN 1.0 ELSE 0 END)) as faltan_datos,
            (CASE vc.estatus_gen WHEN 'Faltan datos' THEN 1.0 ELSE 0 END) as faltan_datos_aux,
            count((CASE vc.estatus_gen WHEN 'Completo' THEN 1.0 ELSE 0 END)) as exitoso_registro,
            (CASE vc.estatus_gen WHEN 'Completo' THEN 1.0 ELSE 0 END) as exitoso_registro_aux,
            count(*) as total_registros,
            vc.create_date as fecha,
            count((CASE vc.estatus_gen WHEN 'Rechazado' THEN 1.0 ELSE 0 END)) as rechazo_registro,
            (CASE vc.estatus_gen WHEN 'Rechazado' THEN 1.0 ELSE 0 END) as rechazo_registro_aux
        """
        for field in fields.values():
            select_ += field
        
        from_ = """
                valida_curp_valida_curp vc
                %s
        """ % from_clause

        
        groupby_ = """
            vc.state,
            vc.nombres,
            vc.create_date,
            vc.curp,
            vc.id %s
        """ % (groupby)
        
        return '%s (SELECT %s FROM %s WHERE vc.state IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)
    
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))